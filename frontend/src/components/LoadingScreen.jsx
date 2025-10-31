function LoadingScreen() {
  return (
    <div className="screen">
      <h1>✨ AI 이미지 생성 중...</h1>
      <p>잠시만 기다려주세요</p>
      <div className="loading-spinner"></div>
      <p style={{ fontSize: '18px', opacity: 0.8 }}>
        나는 솔로 스타일의 멋진 사진을 만들고 있습니다
      </p>
    </div>
  )
}

export default LoadingScreen
