import { QRCodeSVG } from 'qrcode.react'

function ProfileResultScreen({ imageUrl, onNext, onReset }) {
  // QR 코드에 들어갈 URL (실제로는 백엔드에서 생성한 이미지 호스팅 URL)
  const downloadUrl = imageUrl || 'https://example.com/download/profile123'

  return (
    <div className="screen">
      <h1>🎭 나는 솔로 프로필 완성!</h1>
      <p>당신의 나는 솔로 프로필이 완성되었습니다</p>

      <img
        src={imageUrl}
        alt="생성된 프로필"
        className="result-image"
      />

      <div className="qr-code">
        <QRCodeSVG value={downloadUrl} size={200} />
        <p style={{ color: '#667eea', marginTop: '10px', fontSize: '16px' }}>
          QR 코드를 스캔하여 이미지 다운로드
        </p>
      </div>

      <div className="button-group">
        <button className="button secondary" onClick={onReset}>
          🏠 처음으로
        </button>
        <button className="button" onClick={onNext}>
          계속 진행 (장기자랑) →
        </button>
      </div>
    </div>
  )
}

export default ProfileResultScreen
