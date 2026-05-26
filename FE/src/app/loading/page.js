"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { uploadStore } from "../lib/upload-store";

const BLADE_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315];

function Spinner() {
  return (
    <div className="mb-10">
      <svg
        viewBox="0 0 100 100"
        width="140"
        height="140"
        className="animate-spin"
        style={{ animationDuration: "1.8s" }}
        aria-hidden="true"
      >
        {BLADE_ANGLES.map((angle) => (
          <rect
            key={angle}
            x="46"
            y="6"
            width="12"
            height="22"
            rx="5"
            fill="white"
            transform={`rotate(${angle} 50 50)`}
          />
        ))}
      </svg>
    </div>
  );
}

export default function Loading() {
  const [percent, setPercent] = useState(0);
  const [status, setStatus] = useState("동영상 업로드 중...");
  const router = useRouter();

  useEffect(() => {
    if (!uploadStore.promise) {
      router.push("/edit");
      return;
    }

    uploadStore.promise.then(async (uploadResult) => {
      uploadStore.videoInfo = uploadResult;
      setPercent(50);
      setStatus("동영상 분석 중...");
      const { video_id } = uploadResult;

      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ video_id }),
      });
      const { segments } = await res.json();
      uploadStore.segments = segments;

      setPercent(100);
      router.push("/edit");
    });
  }, []);

  return (
    <div className="min-h-screen overflow-hidden bg-gradient-to-br from-[#180028] via-[#08000f] to-black text-white px-4 py-6">
      <link
        href="https://api.fontshare.com/v2/css?f[]=nippo@700,900&display=swap"
        rel="stylesheet"
      />

      <header className="flex items-center gap-6">
        <Link href="/">
          <h1
            className="text-[41px] font-black tracking-[0.08em] hover:opacity-80  -translate-y-2"
            style={{ fontFamily: "'Nippo', sans-serif" }}
          >
            VIBE-WRITER
          </h1>
        </Link>

        <p className="text-[18px] text-white/80 tracking-wide">
          AI 감정 기반 숏폼 자막 자동 생성 서비스
        </p>
      </header>

      <div className="-mx-8 mt-1 border-b-2 border-white/80" />

      <main className="flex justify-center mt-24">
        <div className="w-full max-w-[530px] h-[500px] rounded-[60px] border-[6px] border-white/80 bg-gradient-to-b from-[#190022] via-[#1e1b27] to-[#3B3B3B] flex flex-col items-center justify-center">
          <Spinner />
          {/*박스 크기 수정 필요*/}

          <p className="text-[20px] mb-10 tracking-wide text-center">
            AI가 감정을 분석하고 자막을 생성하는 중이에요
          </p>

          <div className="w-[380px] h-[15px] rounded-full bg-white/25 overflow-hidden">
            <div
              className="h-full rounded-full bg-white"
              style={{ width: `${percent}%` }}
            />
          </div>

          <p className="text-[19px] mt-7 tracking-wide text-white/90">
            {status} {percent}%
          </p>
        </div>
      </main>
    </div>
  );
}
