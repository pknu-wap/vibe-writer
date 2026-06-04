"use client";
import { useRouter } from "next/navigation";
import TopNav from "../components/top-nav";
import { uploadStore } from "../lib/upload-store";
import { API_BASE } from "../lib/api";

export default function DownloadPage() {
  const router = useRouter();
  const videoId = uploadStore.videoInfo?.video_id;
  const videoSrc = videoId ? `${API_BASE}/videos/${videoId}` : null;

  const handleVideoDownload = () => {
    if (!videoId) return;
    const a = document.createElement("a");
    a.href = `${API_BASE}/download?video_id=${videoId}`;
    a.download = `vibe_writer_${videoId}.mp4`;
    a.click();
  };

  const handleAssDownload = () => {
    if (!videoId) return;
    const a = document.createElement("a");
    a.href = `${API_BASE}/download-ass?video_id=${videoId}`;
    a.download = `vibe_writer_${videoId}.ass`;
    a.click();
  };

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-[#190022] via-[#0d0014] to-black flex flex-col">
      <TopNav />
      <main className="flex flex-1 items-center justify-between px-70">

        <div className="flex flex-col">
          <div className="w-[276px] h-[588px] bg-black border-4 border-black rounded-2xl overflow-hidden">
            {videoSrc ? (
              <video
                src={videoSrc}
                className="w-full h-full object-cover"
                controls
                muted
              />
            ) : (
              <div className="w-full h-full bg-white rounded-2xl" />
            )}
          </div>
        </div>

        <div className="flex flex-col gap-6 w-[560px]">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-[#00FF37] flex items-center justify-center flex-shrink-0">
              <svg width="22" height="20" viewBox="0 0 22 20" fill="none">
                <path d="M2 10L8.5 17L20 3" stroke="white" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <span className="text-white font-black text-5xl">완성됐어요!</span>
          </div>

          <button
            onClick={handleVideoDownload}
            className="w-full h-32 bg-black border-4 border-white rounded-2xl text-white font-black text-3xl hover:bg-white hover:text-black transition-colors duration-200"
          >
            다운로드
          </button>

          <button
            onClick={handleAssDownload}
            className="w-full h-32 bg-black border-4 border-white rounded-2xl text-white font-black text-3xl hover:bg-white hover:text-black transition-colors duration-200"
          >
            자막파일(.ASS)다운로드
          </button>

          <button
            onClick={() => router.push("/edit")}
            className="w-full h-32 bg-white border-4 border-black rounded-2xl text-black font-black text-3xl flex items-center justify-center hover:bg-black hover:text-white transition-colors duration-200"
          >
            다시 편집하기
          </button>
        </div>

      </main>
    </div>
  );
}