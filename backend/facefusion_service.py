"""
FaceFusion 실행 서비스

facefusion 모듈을 직접 import하여 실제 얼굴 합성을 수행합니다.
모델을 메모리에 한 번만 로드하고 재사용하여 효율적으로 처리합니다.
"""

import sys
import logging
from pathlib import Path
from typing import Optional

from backend.core.config import settings

logger = logging.getLogger(__name__)


class FaceFusionService:
    """FaceFusion 실행 서비스 클래스"""

    def __init__(self):
        """FaceFusion 서비스 초기화"""
        self.mode = settings.facefusion.mode
        self.facefusion_path = Path(settings.facefusion.project_path).resolve()
        self.face_swapper_model = settings.facefusion.face_swapper_model
        self.execution_providers = settings.facefusion.execution_providers

        # facefusion 모듈 import를 위한 경로 추가
        if str(self.facefusion_path) not in sys.path:
            sys.path.insert(0, str(self.facefusion_path))

        # facefusion 모듈 초기화 (real 모드일 때만)
        self._facefusion_initialized = False
        self._state_manager = None
        self._image_to_image = None

        if self.mode == "real":
            self._initialize_facefusion()

        logger.info(f"FaceFusion 서비스 초기화 완료")
        logger.info(f"Mode: {self.mode}")
        logger.info(f"FaceFusion path: {self.facefusion_path}")

    def _initialize_facefusion(self):
        """FaceFusion 모듈 초기화"""
        try:
            logger.info(f"FaceFusion 모듈 import 시작... (path: {self.facefusion_path})")

            # facefusion 모듈 import
            from facefusion import state_manager
            from facefusion.workflows import image_to_image
            from facefusion import logger as ff_logger

            self._state_manager = state_manager
            self._image_to_image = image_to_image

            logger.info("FaceFusion 모듈 import 성공")

            # FaceFusion 로거 설정 (선택사항)
            # ff_logger.init('info')

            # 기본 설정 초기화
            logger.info("FaceFusion 기본 설정 초기화 시작...")
            self._init_default_state()
            logger.info("FaceFusion 기본 설정 초기화 완료")

            self._facefusion_initialized = True
            logger.info("✅ FaceFusion 모듈 초기화 완료")

        except ImportError as e:
            logger.error(f"❌ FaceFusion 모듈 import 실패: {e}")
            logger.error(f"PYTHONPATH에 {self.facefusion_path}가 추가되었는지 확인하세요")
            raise RuntimeError(f"FaceFusion 모듈을 찾을 수 없습니다: {e}")
        except Exception as e:
            logger.error(f"❌ FaceFusion 초기화 중 오류: {e}")
            import traceback
            logger.error(traceback.format_exc())
            raise

    def _init_default_state(self):
        """FaceFusion state manager 기본 설정"""
        # 프로세서 설정
        self._state_manager.init_item('processors', ['face_swapper'])

        # Face swapper 모델 설정
        self._state_manager.init_item('face_swapper_model', self.face_swapper_model)

        # Execution provider 설정
        self._state_manager.init_item('execution_providers', self.execution_providers)
        self._state_manager.init_item('execution_device_ids', ['0'])  # CPU 또는 GPU 디바이스 ID (문자열 리스트)
        self._state_manager.init_item('execution_thread_count', 8)  # 실행 스레드 수
        self._state_manager.init_item('execution_queue_count', 1)

        # Download 설정 (NSFW 체크 등에 필요)
        self._state_manager.init_item('download_providers', ['github'])
        self._state_manager.init_item('download_scope', 'full')

        # Face detector 설정
        self._state_manager.init_item('face_detector_model', 'yolo_face')
        self._state_manager.init_item('face_detector_size', '640x640')
        self._state_manager.init_item('face_detector_score', 0.5)
        self._state_manager.init_item('face_detector_angles', [0])
        self._state_manager.init_item('face_detector_margin', [0, 0, 0, 0])

        # Face landmarker 설정
        self._state_manager.init_item('face_landmarker_model', '2dfan4')
        self._state_manager.init_item('face_landmarker_score', 0.5)

        # Face selector 설정
        self._state_manager.init_item('face_selector_mode', 'reference')
        self._state_manager.init_item('face_selector_order', 'large-small')
        self._state_manager.init_item('face_selector_age_start', None)
        self._state_manager.init_item('face_selector_age_end', None)
        self._state_manager.init_item('face_selector_gender', None)
        self._state_manager.init_item('face_selector_race', None)
        self._state_manager.init_item('reference_face_position', 0)
        self._state_manager.init_item('reference_face_distance', 0.3)
        self._state_manager.init_item('reference_frame_number', 0)

        # Face masker 설정
        self._state_manager.init_item('face_mask_types', ['box'])
        self._state_manager.init_item('face_mask_blur', 0.3)
        self._state_manager.init_item('face_mask_padding', [0, 0, 0, 0])
        self._state_manager.init_item('face_mask_regions', [])
        self._state_manager.init_item('face_mask_areas', [])
        self._state_manager.init_item('face_occluder_model', 'xseg_1')
        self._state_manager.init_item('face_parser_model', 'bisenet_resnet_34')

        # Face swapper 추가 설정
        self._state_manager.init_item('face_swapper_pixel_boost', '128x128')
        self._state_manager.init_item('face_swapper_weight', 1.0)

        # Memory 설정
        self._state_manager.init_item('video_memory_strategy', 'strict')
        self._state_manager.init_item('system_memory_limit', 0)

        # Output 설정
        self._state_manager.init_item('output_image_quality', 80)
        self._state_manager.init_item('output_image_scale', 1.0)

        # Temp 설정
        self._state_manager.init_item('temp_path', '.facefusion')  # Temp 디렉토리 경로
        self._state_manager.init_item('temp_frame_format', 'jpg')
        self._state_manager.init_item('keep_temp', False)

        # 기타 필수 설정
        self._state_manager.init_item('log_level', 'error')

        logger.debug("FaceFusion 기본 설정 완료")

    async def generate_image(
        self,
        source_path: str,
        target_path: str,
        output_path: str
    ) -> None:
        """
        얼굴 합성 이미지 생성

        source_path의 얼굴을 target_path의 이미지에 합성하여 output_path에 저장합니다.

        Args:
            source_path: 원본 이미지 경로 (사용자가 업로드한 이미지)
            target_path: 타겟 이미지 경로 (프로필 또는 탤런트 이미지)
            output_path: 출력 이미지 경로

        Raises:
            FileNotFoundError: 입력 파일이 존재하지 않음
            RuntimeError: FaceFusion 실행 실패
        """
        if self.mode == "mock":
            logger.warning("Mock mode: Face fusion is disabled, using mock implementation")
            await self._mock_generate_image(source_path, target_path, output_path)
            return

        # 파일 경로 검증
        source_file = Path(source_path)
        target_file = Path(target_path)
        output_file = Path(output_path)

        # 상대 경로를 절대 경로로 변환
        if not source_file.is_absolute():
            source_file = Path.cwd() / source_file
        if not target_file.is_absolute():
            target_file = Path.cwd() / target_file

        if not source_file.exists():
            raise FileNotFoundError(f"Source image not found: {source_file}")
        if not target_file.exists():
            raise FileNotFoundError(f"Target image not found: {target_file}")

        # 출력 디렉토리 생성
        output_file.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Starting face fusion:")
        logger.info(f"  Source: {source_file}")
        logger.info(f"  Target: {target_file}")
        logger.info(f"  Output: {output_file}")

        try:
            # FaceFusion state 설정
            logger.info("Setting FaceFusion state...")
            self._state_manager.set_item('source_paths', [str(source_file)])
            self._state_manager.set_item('target_path', str(target_file))
            self._state_manager.set_item('output_path', str(output_file))
            logger.info("FaceFusion state set successfully")

            # 얼굴 합성 실행
            import time
            start_time = time.time()

            logger.info("Starting FaceFusion image_to_image.process()...")
            error_code = self._image_to_image.process(start_time)
            logger.info(f"FaceFusion process returned error code: {error_code}")

            if error_code != 0:
                raise RuntimeError(f"FaceFusion failed with error code: {error_code}")

            # 출력 파일 생성 확인
            if not output_file.exists():
                raise RuntimeError(f"Output file not created: {output_file}")

            elapsed = time.time() - start_time
            logger.info(f"✅ Face fusion completed successfully in {elapsed:.2f}s: {output_file}")

        except Exception as e:
            logger.error(f"❌ Face fusion failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            raise RuntimeError(f"Face fusion failed: {str(e)}") from e

    async def _mock_generate_image(
        self,
        source_path: str,
        target_path: str,
        output_path: str
    ) -> None:
        """
        모의 이미지 생성 (mock mode)

        실제 FaceFusion을 실행하지 않고 타겟 이미지를 복사합니다.
        """
        import shutil
        import asyncio

        logger.info("Mock mode: Copying target image to output")

        target_file = Path(target_path)
        output_file = Path(output_path)

        # 상대 경로를 절대 경로로 변환
        if not target_file.is_absolute():
            target_file = Path.cwd() / target_file

        if not target_file.exists():
            raise FileNotFoundError(f"Target image not found: {target_file}")

        # 출력 디렉토리 생성
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # 타겟 이미지 복사 (모의 실행)
        shutil.copy2(target_file, output_file)

        # AI 처리 시뮬레이션
        await asyncio.sleep(2.0)

        logger.info(f"Mock face fusion completed: {output_file}")
