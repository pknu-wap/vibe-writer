"use client";

import { useRef } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Upload() {
  const router = useRouter();
  const fileInputRef = useRef(null);

  const handleFile = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    router.push("/loading");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#190022] to-black">
      <header className="flex items-baseline gap-4 px-8 py-6">
        <Link href="/">
          <h1 className="text-3xl font-black tracking-wide text-white hover:opacity-80 transition-opacity cursor-pointer">
            VIBE - WRITER
          </h1>
        </Link>
        <p className="text-sm text-white/80">
          AI 감정 기반 숏폼 자막 자동 생성 서비스
        </p>
      </header>

      <main className="flex flex-col items-center px-8 mt-8">
        <h2 className="text-7xl font-black text-white tracking-tight mb-12">
          VIBE - WRITER
        </h2>

        <div className="w-[500px] aspect-[4/5] rounded-3xl border border-white/30 bg-gradient-to-b from-zinc-700/30 to-zinc-900/50 shadow-2xl flex flex-col items-center justify-center px-12 gap-8">
          <div className="w-32 h-32 rounded-full border-4 border-white flex items-center justify-center bg-[#190022]">
            <svg
              width="56"
              height="56"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-white"
            >
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
          </div>

          <div className="text-center">
            <p className="text-xl font-bold text-white">
              영상을 여기에 첨부 해 주세요.
            </p>
            <p className="text-sm text-white/60 mt-2">
              새로형(9:16), 60초 이내, MP4
            </p>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept="video/mp4"
            className="hidden"
            onChange={handleFile}
          />
          <button
            onClick={() => fileInputRef.current?.click()}
            className="px-16 py-3 rounded-full bg-[#190022] border border-white/30 text-white text-lg font-bold hover:bg-[#2a0040] transition-colors cursor-pointer"
          >
            영상 선택하기
          </button>
        </div>
      </main>
    </div>
  );
}
