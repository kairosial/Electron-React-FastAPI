import { QRCodeSVG } from 'qrcode.react'

function TalentResultScreen({ imageUrl, onReset }) {
  // QR 코드에 들어갈 URL (실제로는 백엔드에서 생성한 이미지 호스팅 URL)
  const downloadUrl = imageUrl || 'https://example.com/download/talent123'

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-10 bg-gradient-to-br from-primary to-secondary text-white">
      <h1 className="text-5xl mb-8 text-center font-bold">🎪 나는 솔로 장기자랑 완성!</h1>
      <p className="text-2xl mb-5 text-center leading-relaxed">당신의 나는 솔로 장기자랑 사진이 완성되었습니다</p>

      <img
        src={imageUrl}
        alt="생성된 장기자랑 사진"
        className="max-w-[600px] max-h-[600px] rounded-2xl shadow-[0_10px_40px_rgba(0,0,0,0.3)] my-5"
      />

      <div className="bg-white p-5 rounded-2xl my-5">
        <QRCodeSVG value={downloadUrl} size={200} />
        <p className="text-primary mt-2.5 text-base">
          QR 코드를 스캔하여 이미지 다운로드
        </p>
      </div>

      <div className="flex gap-5 mt-8">
        <button
          className="px-16 py-5 text-2xl bg-white text-primary border-0 rounded-full font-bold transition-all duration-300 my-2.5 cursor-pointer hover:scale-105 hover:shadow-[0_10px_30px_rgba(0,0,0,0.3)] active:scale-95"
          onClick={onReset}
        >
          🏠 처음으로 돌아가기
        </button>
      </div>

      <p className="text-lg mt-8 opacity-90">
        체험해 주셔서 감사합니다! 😊
      </p>
    </div>
  )
}

export default TalentResultScreen
