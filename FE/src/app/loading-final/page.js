"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

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
  const [percent, setPercent] = useState(1);

  useEffect(() => {
    const timer = setInterval(() => {
      setPercent((prev) => {
        if (prev >= 100) return 100;
        return prev + 1;
      });
    }, 45);

    return () => clearInterval(timer);
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

      <div className='-mx-8 mt-1 border-b-2 border-white/80' />

      <main className="flex justify-center mt-24">
        <div className="w-full max-w-[530px] h-[500px] rounded-[60px] border-[6px] border-white/80 bg-gradient-to-b from-[#190022] via-[#1e1b27] to-[#3B3B3B] flex flex-col items-center justify-center">
          <Spinner />
          {/*박스 크기 및 색상 수정 필요*/}

          <p className="text-[20px] mb-10 tracking-wide text-center">
            자막을 영상에 입히는 중이에요
            <br />
            잠시만 기다려주세요
          </p>

          <div className="w-[380px] h-[15px] rounded-full bg-white/25 overflow-hidden">
            <div
              className="h-full rounded-full bg-white"
              style={{ width: `${percent}%` }}
            />
          </div>

          <p className="text-[19px] mt-7 tracking-wide text-white/90">
            자막 입히는 중 ... {percent}%
          </p>
        </div>
      </main>
    </div>
  );
}