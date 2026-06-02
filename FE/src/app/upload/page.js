"use client";
import "./upload.css";
import TopNav from "../components/top-nav";
import { useRouter } from "next/navigation";
// TODO: 프로젝트의 실제 uploadStore 경로에 맞게 임포트 경로를 수정하세요.
import { useUploadStore } from "@/store/uploadStore"; 

export default function UploadPage() {
  const router = useRouter();
  // uploadStore에서 video_id를 저장할 수 있는 액션 함수를 가져옵니다.
  // (스토어 내부의 함수명이 setVideoId가 아니라면 맞춰서 변경해주세요)
  const { setVideoId } = useUploadStore();

  const handleFilechange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("video", file);

    try {
      // 1. [수정] 외부 포트 직접 호출 대신 Next.js API 라우터 경유 (/api/upload)
      const response = await fetch("/api/upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("업로드 실패");
      }

      // 2. [추가] 백엔드 응답 데이터 파싱 및 uploadStore에 video_id 저장
      const data = await response.json();
      if (data && data.video_id) {
        setVideoId(data.video_id);
      }

      // 성공 시 로딩 페이지로 이동
      router.push("/loading");

    } catch (error) {
      console.error("Upload Error:", error);
      alert("영상 업로드 중 오류가 발생했습니다.");
    }
  };

  return (
    <div className="upload-container">
      <TopNav />

      <main className="main">
        <h1 className="upload-main-title">VIBE - WRITER</h1>

        <div className="upload-card">
          <div className="upload-circle">
            <svg
              width="100"
              height="100"
              viewBox="0 0 100 100"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M50 75L18.75 43.75L27.5 34.6875L43.75 50.9375V0H56.25V50.9375L72.5 34.6875L81.25 43.75L50 75ZM12.5 100C9.0625 100 6.12083 98.7771 3.675 96.3313C1.22917 93.8854 0.00416667 90.9417 0 87.5V68.75H12.5V87.5H87.5V68.75H100V87.5C100 90.9375 98.7771 93.8812 96.3313 96.3313C93.8854 98.7812 90.9417 100.004 87.5 100H12.5Z"
                fill="white"
              />
            </svg>
          </div>

          <h2 className="upload-title">
            영상을 여기에 첨부 해 주세요.
          </h2>

          <p className="upload-desc">
            세로형(9:16), 60초 이내, MP4
          </p>

          <input
            type="file"
            accept="video/mp4"
            id="video-upload"
            hidden
            onChange={handleFilechange}
          />

          <label
            htmlFor="video-upload"
            className="upload-button"
          >
            영상 선택하기
          </label>
        </div>
      </main>
    </div>
  );
}