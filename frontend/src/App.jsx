import { useState } from "react";
import ConsentScreen from "./components/ConsentScreen";
import CameraScreen from "./components/CameraScreen";
import LoadingScreen from "./components/LoadingScreen";
import ProfileResultScreen from "./components/ProfileResultScreen";
import TalentResultScreen from "./components/TalentResultScreen";

function App() {
  // 현재 화면 상태 관리
  // 1: 동의서, 2: 촬영, 3: 로딩, 4: 프로필 결과, 5: 장기자랑 결과
  const [currentScreen, setCurrentScreen] = useState(1);

  // 촬영된 이미지 저장
  const [capturedImage, setCapturedImage] = useState(null);

  // 생성된 이미지 URL (백엔드에서 받을 예정)
  const [profileImageUrl, setProfileImageUrl] = useState(null);
  const [talentImageUrl, setTalentImageUrl] = useState(null);

  // 동의서 화면 -> 촬영 화면
  const handleConsentAgree = () => {
    setCurrentScreen(2);
  };

  // 촬영 완료 -> 로딩 화면
  const handleCapture = (imageSrc) => {
    setCapturedImage(imageSrc);
    setCurrentScreen(3);

    // 실제로는 여기서 백엔드 API 호출
    // 지금은 3초 후 프로필 결과 화면으로 이동 (테스트용)
    setTimeout(() => {
      // 더미 이미지 URL (나중에 백엔드 응답으로 교체)
      setProfileImageUrl(imageSrc); // 일단 촬영한 이미지 사용
      setCurrentScreen(4);
    }, 3000);
  };

  // 프로필 결과 -> 장기자랑 생성
  const handleGenerateTalent = () => {
    setCurrentScreen(3); // 다시 로딩 화면

    // 실제로는 백엔드 API 호출
    setTimeout(() => {
      setTalentImageUrl(capturedImage); // 더미
      setCurrentScreen(5);
    }, 3000);
  };

  // 처음으로 돌아가기
  const handleReset = () => {
    setCurrentScreen(1);
    setCapturedImage(null);
    setProfileImageUrl(null);
    setTalentImageUrl(null);
  };

  // 화면별 렌더링
  return (
    <>
      {currentScreen === 1 && <ConsentScreen onAgree={handleConsentAgree} />}
      {currentScreen === 2 && <CameraScreen onCapture={handleCapture} />}
      {currentScreen === 3 && <LoadingScreen />}
      {currentScreen === 4 && (
        <ProfileResultScreen
          imageUrl={profileImageUrl}
          onNext={handleGenerateTalent}
          onReset={handleReset}
        />
      )}
      {currentScreen === 5 && (
        <TalentResultScreen imageUrl={talentImageUrl} onReset={handleReset} />
      )}
    </>
  );
}

export default App;
