import { useRef, useState } from 'react'
import Webcam from 'react-webcam'

function CameraScreen({ onCapture }) {
  const webcamRef = useRef(null)
  const [isCaptured, setIsCaptured] = useState(false)
  const [capturedImage, setCapturedImage] = useState(null)

  // 웹캠 설정
  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: 'user'
  }

  // 촬영 버튼 클릭
  const handleCaptureClick = () => {
    const imageSrc = webcamRef.current.getScreenshot()
    setCapturedImage(imageSrc)
    setIsCaptured(true)
  }

  // 재촬영
  const handleRetake = () => {
    setIsCaptured(false)
    setCapturedImage(null)
  }

  // 확인 버튼
  const handleConfirm = () => {
    onCapture(capturedImage)
  }

  return (
    <div className="screen">
      <h1>📸 사진 촬영</h1>
      <p>화면 중앙에 얼굴이 잘 보이도록 위치해주세요</p>

      <div className="webcam-container">
        {!isCaptured ? (
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            className="webcam-preview"
          />
        ) : (
          <img src={capturedImage} alt="촬영된 사진" className="webcam-preview" />
        )}
      </div>

      <div className="button-group">
        {!isCaptured ? (
          <button className="button" onClick={handleCaptureClick}>
            📷 촬영하기
          </button>
        ) : (
          <>
            <button className="button secondary" onClick={handleRetake}>
              🔄 다시 촬영
            </button>
            <button className="button" onClick={handleConfirm}>
              ✅ 이 사진으로 진행
            </button>
          </>
        )}
      </div>
    </div>
  )
}

export default CameraScreen
