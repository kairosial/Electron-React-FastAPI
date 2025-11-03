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
    <div className="w-full h-full flex flex-col items-center justify-center p-10 bg-gradient-to-br from-primary to-secondary text-white">
      <h1 className="text-5xl mb-8 text-center font-bold">📸 사진 촬영</h1>
      <p className="text-2xl mb-5 text-center leading-relaxed">화면 중앙에 얼굴이 잘 보이도록 위치해주세요</p>

      <div className="relative rounded-2xl overflow-hidden shadow-[0_10px_40px_rgba(0,0,0,0.3)] my-8">
        {!isCaptured ? (
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            videoConstraints={videoConstraints}
            className="rounded-2xl"
          />
        ) : (
          <img src={capturedImage} alt="촬영된 사진" className="rounded-2xl" />
        )}
      </div>

      <div className="flex gap-5 mt-8">
        {!isCaptured ? (
          <button
            className="px-16 py-5 text-2xl bg-white text-primary border-0 rounded-full font-bold transition-all duration-300 my-2.5 cursor-pointer hover:scale-105 hover:shadow-[0_10px_30px_rgba(0,0,0,0.3)] active:scale-95"
            onClick={handleCaptureClick}
          >
            📷 촬영하기
          </button>
        ) : (
          <>
            <button
              className="px-16 py-5 text-2xl bg-transparent text-white border-4 border-white rounded-full font-bold transition-all duration-300 my-2.5 cursor-pointer hover:scale-105 hover:shadow-[0_10px_30px_rgba(0,0,0,0.3)] active:scale-95"
              onClick={handleRetake}
            >
              🔄 다시 촬영
            </button>
            <button
              className="px-16 py-5 text-2xl bg-white text-primary border-0 rounded-full font-bold transition-all duration-300 my-2.5 cursor-pointer hover:scale-105 hover:shadow-[0_10px_30px_rgba(0,0,0,0.3)] active:scale-95"
              onClick={handleConfirm}
            >
              ✅ 이 사진으로 진행
            </button>
          </>
        )}
      </div>
    </div>
  )
}

export default CameraScreen
