"use client";

import { useRouter } from "next/navigation";
import TopNav from "../components/top-nav";
import { uploadStore } from "../lib/upload-store";
import "./download.css";

export default function DownloadPage() {
  const router = useRouter();
  const videoId = uploadStore.videoInfo?.video_id;
  const videoSrc = videoId ? `/api/video/${videoId}` : null;

  const handleVideoDownload = () => {
    if (!videoId) return;
    const a = document.createElement("a");
    a.href = `/api/download?video_id=${videoId}`;
    a.download = `vibe_writer_${videoId}.mp4`;
    a.click();
  };

  const handleSrtDownload = () => {
    const a = document.createElement("a");
    a.href = `/api/download-srt?video_id=${videoId}`;
    a.download = "subtitles.srt";
    a.click();
  };

  return (
    <div className="download-container">
      <TopNav />

      <div className="download-body">
        {/* Left: video preview */}
        <div className="download-video-wrap">
          <video
            src={videoSrc}
            className="download-video"
            controls={false}
            muted
          />
        </div>

        {/* Right: actions */}
        <div className="download-actions">
          <div className="done-heading">
            <span className="done-check">✓</span>
            <span className="done-text">완성됐어요!</span>
          </div>

          <button className="action-btn dark" onClick={handleVideoDownload}>
            다운로드
          </button>

          <button className="action-btn dark" onClick={handleSrtDownload}>
            자막파일(.SRT)다운로드
          </button>

          <button
            className="action-btn light"
            onClick={() => router.push("/edit")}
          >
            다시 편집하기
          </button>
        </div>
      </div>
    </div>
  );
}
