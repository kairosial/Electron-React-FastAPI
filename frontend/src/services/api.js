/**
 * 백엔드 API 통신 서비스
 * FastAPI 백엔드와의 이미지 업로드 및 처리 요청을 담당합니다.
 */

const API_BASE_URL = 'http://localhost:8000'

/**
 * base64 이미지 데이터를 Blob으로 변환
 * @param {string} base64Data - base64 인코딩된 이미지 데이터
 * @returns {Blob} 이미지 Blob 객체
 */
function base64ToBlob(base64Data) {
  // data:image/jpeg;base64, 부분 제거
  const base64String = base64Data.split(',')[1]
  const byteCharacters = atob(base64String)
  const byteNumbers = new Array(byteCharacters.length)

  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i)
  }

  const byteArray = new Uint8Array(byteNumbers)
  return new Blob([byteArray], { type: 'image/jpeg' })
}

/**
 * 프로필 이미지 생성 요청
 * @param {string} imageData - base64 인코딩된 이미지 데이터
 * @returns {Promise<{imageUrl: string, filename: string}>} 생성된 이미지 정보
 */
export async function generateProfileImage(imageData) {
  try {
    // FormData 생성
    const formData = new FormData()
    const blob = base64ToBlob(imageData)
    formData.append('file', blob, 'captured_image.jpg')

    // API 요청
    const response = await fetch(`${API_BASE_URL}/api/generate/profile`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`서버 오류: ${response.status} ${response.statusText}`)
    }

    const data = await response.json()

    if (!data.success) {
      throw new Error(data.message || '이미지 생성에 실패했습니다.')
    }

    return {
      imageUrl: data.image_url,
      filename: data.filename,
    }
  } catch (error) {
    console.error('프로필 이미지 생성 실패:', error)
    throw new Error(
      `프로필 이미지 생성에 실패했습니다.\n백엔드 서버가 실행 중인지 확인해주세요.\n\n오류: ${error.message}`
    )
  }
}

/**
 * 탤런트쇼 이미지 생성 요청
 * @param {string} imageData - base64 인코딩된 이미지 데이터
 * @returns {Promise<{imageUrl: string, filename: string}>} 생성된 이미지 정보
 */
export async function generateTalentImage(imageData) {
  try {
    // FormData 생성
    const formData = new FormData()
    const blob = base64ToBlob(imageData)
    formData.append('file', blob, 'captured_image.jpg')

    // API 요청
    const response = await fetch(`${API_BASE_URL}/api/generate/talent`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`서버 오류: ${response.status} ${response.statusText}`)
    }

    const data = await response.json()

    if (!data.success) {
      throw new Error(data.message || '이미지 생성에 실패했습니다.')
    }

    return {
      imageUrl: data.image_url,
      filename: data.filename,
    }
  } catch (error) {
    console.error('탤런트쇼 이미지 생성 실패:', error)
    throw new Error(
      `탤런트쇼 이미지 생성에 실패했습니다.\n백엔드 서버가 실행 중인지 확인해주세요.\n\n오류: ${error.message}`
    )
  }
}

/**
 * 서버 상태 확인
 * @returns {Promise<boolean>} 서버 실행 여부
 */
export async function checkServerHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
    })
    return response.ok
  } catch (error) {
    console.error('서버 연결 실패:', error)
    return false
  }
}
