"use client";
import "./upload.css";
import TopNav from "../components/top-nav";
import { useRouter } from "next/navigation";

export default function UploadPage() {

  const router = useRouter();

  const handleFilechange = async (e) => {
    const file = e.target.files[0];

    if (!file) return;


    const formData = new FormData();

    formData.append("video", file);

    const response = await fetch(
      "http://localhost:8080/upload",
      {
        method: "POST",
        body:formData,

      }
    );
    router.push("/loading");

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
            세로형(9:16),60초 이내,MP4
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