import { useState } from 'react'

function ConsentScreen({ onAgree }) {
  const [personalInfoConsent, setPersonalInfoConsent] = useState(false)
  const [portraitRightsConsent, setPortraitRightsConsent] = useState(false)

  const canProceed = personalInfoConsent && portraitRightsConsent

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-10 bg-gradient-to-br from-primary to-secondary text-white">
      <h1 className="text-5xl mb-8 text-center font-bold">🎬 나는 솔로 체험을 시작합니다</h1>
      <p className="text-2xl mb-5 text-center leading-relaxed">체험을 진행하기 위해 아래 동의가 필요합니다</p>

      <div className="bg-white/10 p-8 rounded-2xl my-8 max-w-3xl">
        <div className="flex items-center my-5 text-xl">
          <input
            type="checkbox"
            id="personal-info"
            checked={personalInfoConsent}
            onChange={(e) => setPersonalInfoConsent(e.target.checked)}
            className="w-8 h-8 mr-4 cursor-pointer"
          />
          <label htmlFor="personal-info" className="cursor-pointer">
            개인정보 수집 및 이용에 동의합니다
          </label>
        </div>

        <div className="flex items-center my-5 text-xl">
          <input
            type="checkbox"
            id="portrait-rights"
            checked={portraitRightsConsent}
            onChange={(e) => setPortraitRightsConsent(e.target.checked)}
            className="w-8 h-8 mr-4 cursor-pointer"
          />
          <label htmlFor="portrait-rights" className="cursor-pointer">
            초상권 사용에 동의합니다
          </label>
        </div>
      </div>

      <button
        className={`px-16 py-5 text-2xl bg-white text-primary border-0 rounded-full font-bold transition-all duration-300 my-2.5 ${
          canProceed
            ? 'opacity-100 cursor-pointer hover:scale-105 hover:shadow-[0_10px_30px_rgba(0,0,0,0.3)] active:scale-95'
            : 'opacity-50 cursor-not-allowed'
        }`}
        onClick={onAgree}
        disabled={!canProceed}
      >
        {canProceed ? '다음으로 →' : '모든 항목에 동의해주세요'}
      </button>
    </div>
  )
}

export default ConsentScreen
