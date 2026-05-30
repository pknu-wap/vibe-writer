"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { uploadStore } from "../lib/upload-store";
import TopNav from "../components/top-nav";
const BLADE_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315];

const ANALYZE_TIME = 31000;

const LOADING_MESSAGE = "AI가 감정을 분석하고 자막을 생성하는 중이에요...";

// 임시 API
const ANALYZE_API = "/api/analyze";

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
            x="45"
            y="6"
            width="10"
            height="24"
            rx="6"
            fill="white"
            transform={`rotate(${angle} 50 50)`}
          />
        ))}
      </svg>
    </div>
  );
}

export default function Loading() {
  const router = useRouter();

  const [percent, setPercent] = useState(1);
  const [errorText, setErrorText] = useState("");

  useEffect(() => {
    let isFinished = false;
    const startTime = Date.now();

    const timer = setInterval(() => {
      if (isFinished) return;

      const elapsedTime = Date.now() - startTime;
      const nextPercent = Math.floor((elapsedTime / ANALYZE_TIME) * 100);
      const safePercent = Math.max(1, Math.min(nextPercent, 95));

      setPercent(safePercent);
    }, 200);

    async function requestAnalyze() {
      try {
        const uploadId = sessionStorage.getItem("uploadId");
        const uploadId = sessionStorage.getItem("uploadId");

        if (!uploadId) {
          throw new Error("업로드 ID를 찾을 수 없습니다.");
        }

        const response = await fetch(ANALYZE_API, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            uploadId: uploadId,
          }),
        });

        if (!response.ok) {
          throw new Error("analyze 요청 실패");
        }

        const result = await response.json();

        sessionStorage.setItem("analyzeResult", JSON.stringify(result));

        uploadStore.videoInfo = result.videoInfo ?? {
          video_id: result.video_id ?? uploadId ?? "mock-video",
          duration: result.duration ?? 12,
        };

        uploadStore.segments = result.segments ?? [];

        isFinished = true;
        clearInterval(timer);

        setPercent(100);

        router.replace("/edit");
      } catch (error) {
        isFinished = true;
        clearInterval(timer);

        console.error(error);
        setErrorText("분석 중 오류가 발생했어요. 다시 시도해주세요.");
      }
    }

    requestAnalyze();

    return () => {
      isFinished = true;
      clearInterval(timer);
    };
  }, [router]);

  return (
    <div
     className="min-h-screen overflow-hidden text-white px-4 py-6"
     style={{
      background: "linear-gradient(135deg, #190022 0%, #190022 15%, #000000 100%)",
     }}
 >
      <TopNav />

      <main className="flex justify-center mt-24">
        <div className="w-full max-w-[530px] h-[500px] rounded-[60px] border-[6px] border-white/80 bg-gradient-to-b from-[#190022] via-[#1e1b27] to-[#3B3B3B] flex flex-col items-center justify-center">
          <Spinner />

          <p className="text-[20px] mb-10 tracking-wide text-center leading-relaxed">
            {errorText ? errorText : LOADING_MESSAGE}
          </p>

          <div className="w-[380px] h-[15px] rounded-full bg-white/25 overflow-hidden">
            <div
              className="h-full rounded-full bg-white transition-all duration-300"
              style={{ width: `${percent}%` }}
            />
          </div>

          <p className="text-[19px] mt-7 tracking-wide text-white/90">
            stt 변환 중 ... {percent}%
          </p>
        </div>
      </main>
    </div>
  );
}