import { QRCodeSVG } from 'qrcode.react'

function TalentResultScreen({ imageUrl, onReset }) {
  // QR 코드에 들어갈 URL (실제로는 백엔드에서 생성한 이미지 호스팅 URL)
  const downloadUrl = imageUrl || 'https://example.com/download/talent123'

  return (
    <div className="screen">
      <h1>🎪 나는 솔로 장기자랑 완성!</h1>
      <p>당신의 나는 솔로 장기자랑 사진이 완성되었습니다</p>

      <img
        src={imageUrl}
        alt="생성된 장기자랑 사진"
        className="result-image"
      />

      <div className="qr-code">
        <QRCodeSVG value={downloadUrl} size={200} />
        <p style={{ color: '#667eea', marginTop: '10px', fontSize: '16px' }}>
          QR 코드를 스캔하여 이미지 다운로드
        </p>
      </div>

      <div className="button-group">
        <button className="button" onClick={onReset}>
          🏠 처음으로 돌아가기
        </button>
      </div>

      <p style={{ fontSize: '18px', marginTop: '30px', opacity: 0.9 }}>
        체험해 주셔서 감사합니다! 😊
      </p>
    </div>
  )
}

export default TalentResultScreen
