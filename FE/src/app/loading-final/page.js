"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import TopNav from "../components/top-nav";

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
  const [errorText, setErrorText] = useState("");
  const router = useRouter();

  useEffect(() => {
    let isFinished = false;

    const timer = setInterval(() => {
      if (isFinished) return;

      setPercent((prev) => {
        if (prev >= 95) {
          return 95;
        }

        return prev + 1;
      });
    }, 100);

    async function waitBackendProcess() {
      try {
        // 목 서버 호출 부분
        // 추후 실제 백엔드 API로 변경 필요
        const response = await fetch("/api/final", {
          method: "POST",
        });

        if (!response.ok) {
          throw new Error("백엔드 처리 실패");
        }

        const result = await response.json();

        //목 서버에서 받은 결과 저장
        sessionStorage.setItem("finalResult", JSON.stringify(result));

        isFinished = true;
        clearInterval(timer);

        setPercent(100);

        router.push("/download");
      } catch (error) {
        isFinished = true;
        clearInterval(timer);

        console.error(error);
        setErrorText("영상 처리 중 오류가 발생했어요. \n다시 시도해주세요.");
      }
    }

    waitBackendProcess();

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
      <link
        href="https://api.fontshare.com/v2/css?f[]=nippo@700,900&display=swap"
        rel="stylesheet"
      />

      <TopNav />

      <main className="flex justify-center mt-24">
        <div className="w-full max-w-[530px] h-[500px] rounded-[60px] border-[6px] border-white/80 bg-gradient-to-b from-[#190022] via-[#1e1b27] to-[#3B3B3B] flex flex-col items-center justify-center">
          <Spinner />

          <p className="text-[20px] mb-10 tracking-wide text-center whitespace-pre-line">
            {errorText ? (
              errorText
            ) : (
              <>
                자막을 영상에 입히는 중이에요
                <br />
                잠시만 기다려주세요
              </>
            )}
          </p>

          <div className="w-[380px] h-[15px] rounded-full bg-white/25 overflow-hidden">
            <div
              className="h-full rounded-full bg-white transition-all duration-300"
              style={{ width: `${percent}%` }}
            />
          </div>

          <p className="text-[19px] mt-7 tracking-wide text-white/90">
            {errorText ? "..." : `자막 입히는 중 ... ${percent}%`}
          </p>
        </div>
      </main>
    </div>
  );
}