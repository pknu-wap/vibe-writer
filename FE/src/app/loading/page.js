"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { uploadStore } from "../lib/upload-store";
import TopNav from "../components/top-nav";

const BLADE_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315];

const UPLOAD_API = "/api/upload";
const ANALYZE_API = "/api/analyze";

const LOADING_MESSAGE = "AI가 감정을 분석하고 자막을 생성하는 중이에요";

const MOVE_DELAY = 300;

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

  const [percent, setPercent] = useState(0);
  const [errorText, setErrorText] = useState("");

  useEffect(() => {
    let isCanceled = false;

    async function processVideo() {
      try {
        setPercent(0);

        const file = uploadStore.file;

        if (!file) {
          throw new Error("업로드할 영상 파일을 찾을 수 없습니다.");
        }

        // 1단계: upload API 호출
        const formData = new FormData();
        formData.append("video", file);

        const uploadResponse = await fetch(UPLOAD_API, {
          method: "POST",
          body: formData,
        });

        if (!uploadResponse.ok) {
          throw new Error("upload 요청 실패");
        }

        const uploadResult = await uploadResponse.json();

        const videoId =
          uploadResult.video_id ??
          uploadResult.videoId ??
          uploadResult.videoInfo?.video_id;

        if (!videoId) {
          throw new Error("video_id를 받지 못했습니다.");
        }

        if (isCanceled) return;

        uploadStore.videoInfo = {
          video_id: videoId,
          duration: uploadResult.duration ?? uploadResult.videoInfo?.duration ?? 0,
        };

        sessionStorage.setItem("uploadResult", JSON.stringify(uploadResult));
        sessionStorage.setItem("videoId", videoId);

        // video_id 받으면 50%
        setPercent(50);

        // 2단계: video_id로 analyze API 호출
        const analyzeResponse = await fetch(ANALYZE_API, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            video_id: videoId,
          }),
        });

        if (!analyzeResponse.ok) {
          throw new Error("analyze 요청 실패");
        }

        const analyzeResult = await analyzeResponse.json();

        if (isCanceled) return;

        uploadStore.segments = analyzeResult.segments ?? [];

        uploadStore.videoInfo = {
          ...uploadStore.videoInfo,
          ...(analyzeResult.videoInfo ?? {}),
        };

        sessionStorage.setItem("analyzeResult", JSON.stringify(analyzeResult));

        // 자막 정보 받으면 100%
        setPercent(100);

        setTimeout(() => {
          router.replace("/edit");
        }, MOVE_DELAY);
      } catch (error) {
        if (isCanceled) return;

        console.error(error);
        setErrorText("분석 중 오류가 발생했어요.\n다시 시도해주세요.");
      }
    }

    processVideo();

    return () => {
      isCanceled = true;
    };
  }, [router]);

  return (
    <div className="min-h-screen overflow-hidden text-white px-4 py-6 bg-[linear-gradient(135deg,#190022_0%,#190022_15%,#000000_100%)]">
      <TopNav />

      <main className="flex justify-center mt-24">
        <div className="w-full max-w-[530px] h-[500px] rounded-[60px] border-[6px] border-white/80 bg-gradient-to-b from-[#190022] via-[#1e1b27] to-[#3B3B3B] flex flex-col items-center justify-center">
          <Spinner />

          <p className="text-[20px] mb-10 tracking-wide text-center leading-relaxed whitespace-pre-line">
            {errorText ? errorText : LOADING_MESSAGE}
          </p>

          <div className="w-[380px] h-[15px] rounded-full bg-white/25 overflow-hidden">
            <div
              className="h-full rounded-full bg-white transition-all duration-300"
              style={{ width: `${percent}%` }}
            />
          </div>

          <p className="text-[19px] mt-7 tracking-wide text-white/90">
            {errorText ? "..." : `stt 변환 중 ... ${percent}%`}
          </p>
        </div>
      </main>
    </div>
  );
}