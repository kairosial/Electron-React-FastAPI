"""
초기 데이터 Seed 스크립트

TargetProfile과 TargetTalent 테이블에 샘플 데이터를 입력합니다.
"""

import asyncio
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.database import AsyncSessionLocal
from backend.models.target_profile import TargetProfile
from backend.models.target_talent import TargetTalent


async def seed_profiles():
    """프로필 타겟 샘플 데이터 입력"""
    profiles = [
        {
            "profile_name": "광수",
            "gender_filter": "male",
            "target_image_path": "assets/profile_targets/kwangsu.jpg",
        },
        {
            "profile_name": "영호",
            "gender_filter": "male",
            "target_image_path": "assets/profile_targets/youngho.jpg",
        },
        {
            "profile_name": "순자",
            "gender_filter": "female",
            "target_image_path": "assets/profile_targets/soonja.jpg",
        },
        {
            "profile_name": "영숙",
            "gender_filter": "female",
            "target_image_path": "assets/profile_targets/youngshook.jpg",
        },
    ]

    async with AsyncSessionLocal() as session:
        for profile_data in profiles:
            profile = TargetProfile(**profile_data)
            session.add(profile)

        await session.commit()
        print(f"✅ {len(profiles)}개의 프로필 타겟이 추가되었습니다.")


async def seed_talents():
    """장기자랑 타겟 샘플 데이터 입력"""
    talents = [
        {
            "talent_name": "기타 연주",
            "gender_filter": "male",
            "target_image_path": "assets/talent_targets/guitar_male.jpg",
        },
        {
            "talent_name": "춤 (남자)",
            "gender_filter": "male",
            "target_image_path": "assets/talent_targets/dance_male.jpg",
        },
        {
            "talent_name": "노래 (남자)",
            "gender_filter": "male",
            "target_image_path": "assets/talent_targets/sing_male.jpg",
        },
        {
            "talent_name": "춤 (여자)",
            "gender_filter": "female",
            "target_image_path": "assets/talent_targets/dance_female.jpg",
        },
        {
            "talent_name": "노래 (여자)",
            "gender_filter": "female",
            "target_image_path": "assets/talent_targets/sing_female.jpg",
        },
    ]

    async with AsyncSessionLocal() as session:
        for talent_data in talents:
            talent = TargetTalent(**talent_data)
            session.add(talent)

        await session.commit()
        print(f"✅ {len(talents)}개의 장기자랑 타겟이 추가되었습니다.")


async def main():
    """메인 실행 함수"""
    print("=" * 50)
    print("초기 데이터 Seed 시작")
    print("=" * 50)

    try:
        await seed_profiles()
        await seed_talents()
        print("\n" + "=" * 50)
        print("✅ 모든 초기 데이터가 성공적으로 추가되었습니다!")
        print("=" * 50)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
