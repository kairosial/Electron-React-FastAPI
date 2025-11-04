function LoadingScreen() {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-10 bg-gradient-to-br from-primary to-secondary text-white">
      <h1 className="text-5xl mb-8 text-center font-bold">✨ AI 이미지 생성 중...</h1>
      <p className="text-2xl mb-5 text-center leading-relaxed">잠시만 기다려주세요</p>
      <div className="w-20 h-20 border-8 border-white/30 border-t-white rounded-full animate-spin my-8"></div>
      <p className="text-lg opacity-80">
        나는 솔로 스타일의 멋진 사진을 만들고 있습니다
      </p>
    </div>
  )
}

export default LoadingScreen
