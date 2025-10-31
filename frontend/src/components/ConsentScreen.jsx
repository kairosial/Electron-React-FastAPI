import { useState } from 'react'

function ConsentScreen({ onAgree }) {
  const [personalInfoConsent, setPersonalInfoConsent] = useState(false)
  const [portraitRightsConsent, setPortraitRightsConsent] = useState(false)

  const canProceed = personalInfoConsent && portraitRightsConsent

  return (
    <div className="screen">
      <h1>🎬 나는 솔로 체험을 시작합니다</h1>
      <p>체험을 진행하기 위해 아래 동의가 필요합니다</p>

      <div className="consent-container">
        <div className="consent-item">
          <input
            type="checkbox"
            id="personal-info"
            checked={personalInfoConsent}
            onChange={(e) => setPersonalInfoConsent(e.target.checked)}
          />
          <label htmlFor="personal-info">
            개인정보 수집 및 이용에 동의합니다
          </label>
        </div>

        <div className="consent-item">
          <input
            type="checkbox"
            id="portrait-rights"
            checked={portraitRightsConsent}
            onChange={(e) => setPortraitRightsConsent(e.target.checked)}
          />
          <label htmlFor="portrait-rights">
            초상권 사용에 동의합니다
          </label>
        </div>
      </div>

      <button
        className="button"
        onClick={onAgree}
        disabled={!canProceed}
        style={{
          opacity: canProceed ? 1 : 0.5,
          cursor: canProceed ? 'pointer' : 'not-allowed'
        }}
      >
        {canProceed ? '다음으로 →' : '모든 항목에 동의해주세요'}
      </button>
    </div>
  )
}

export default ConsentScreen
