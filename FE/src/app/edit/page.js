"use client";

import { useState } from "react";
import Link from "next/link";

const emotionPresets = {
  happy: { color: "#f5c542", size: 65, font: "tong", label: "Happy", desc: "노란색 · 65px" },
  angry: { color: "#e05050", size: 70, font: "gak", label: "Angry", desc: "빨간색 · 70px" },
  sad: { color: "#5baef5", size: 45, font: "thin", label: "Sad", desc: "파란색 · 45px" },
  neutral: { color: "#aaaaaa", size: 50, font: "gothic", label: "Neutral", desc: "회색 · 50px" },
};

const fontWeightMap = { tong: 700, gak: 900, thin: 300, gothic: 500 };

export default function Edit() {
  const [fontSize, setFontSize] = useState(28);
  const [position, setPosition] = useState("top");
  const [effect, setEffect] = useState("bounce");
  const [font, setFont] = useState("gothic");
  const [emotion, setEmotion] = useState("happy");
  const [color, setColor] = useState("#ffffff");
  const [showStyle, setShowStyle] = useState(true);
  const [showEmotion, setShowEmotion] = useState(true);

  const selectEmotion = (key) => {
    const p = emotionPresets[key];
    setEmotion(key);
    setColor(p.color);
    setFontSize(p.size);
    setFont(p.font);
  };

  const positionClass = {
    top: "top-4",
    center: "top-1/2 -translate-y-1/2",
    bottom: "bottom-4",
  }[position];

  const effectClass = {
    bounce: "animate-bounce",
    fade: "animate-pulse",
    shake: "animate-[shake_0.4s_ease_infinite]",
    none: "",
  }[effect];

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      <header className="flex items-baseline gap-4 px-8 py-4 border-b border-white/10">
        <Link href="/">
          <h1 className="text-2xl font-black tracking-wide hover:opacity-80 transition-opacity cursor-pointer">
            VIBE - WRITER
          </h1>
        </Link>
        <p className="text-sm text-white/70">AI 감정 기반 숏폼 자막 자동 생성 서비스</p>
        <Link
          href="/download"
          className="ml-auto px-5 py-2 rounded-full bg-white text-black text-sm font-bold hover:bg-white/90 transition-colors self-center"
        >
          편집 완료
        </Link>
      </header>

      <div className="flex-1 grid grid-cols-[280px_1fr_280px]">
        {showStyle ? (
          <aside className="border-r border-white/10 bg-zinc-950 p-5 overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-medium">스타일 설정</h2>
              <button
                onClick={() => setShowStyle(false)}
                className="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-xs cursor-pointer"
              >
                ✕
              </button>
            </div>

            <div className="space-y-6">
              <div>
                <label className="text-xs text-white/50 uppercase tracking-wider">글자 크기</label>
                <div className="flex items-center gap-2 mt-2">
                  <input
                    type="range"
                    min={12}
                    max={70}
                    value={fontSize}
                    onChange={(e) => setFontSize(+e.target.value)}
                    className="range range-xs flex-1"
                  />
                  <span className="text-xs text-white/60 w-10 text-right">{fontSize}px</span>
                </div>
              </div>

              <div>
                <label className="text-xs text-white/50 uppercase tracking-wider">위치</label>
                <div className="flex gap-1 mt-2">
                  {[
                    ["bottom", "하단"],
                    ["center", "중앙"],
                    ["top", "상단"],
                  ].map(([val, lbl]) => (
                    <button
                      key={val}
                      onClick={() => setPosition(val)}
                      className={`px-3 py-1 rounded-full text-xs border cursor-pointer transition-colors ${
                        position === val
                          ? "bg-zinc-700 border-zinc-500 text-white"
                          : "bg-zinc-900 border-zinc-700 text-white/60 hover:border-zinc-500"
                      }`}
                    >
                      {lbl}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs text-white/50 uppercase tracking-wider">효과</label>
                <div className="flex gap-1 mt-2 flex-wrap">
                  {[
                    ["bounce", "바운스"],
                    ["fade", "페이드"],
                    ["shake", "쉐이크"],
                    ["none", "없음"],
                  ].map(([val, lbl]) => (
                    <button
                      key={val}
                      onClick={() => setEffect(val)}
                      className={`px-3 py-1 rounded-full text-xs border cursor-pointer transition-colors ${
                        effect === val
                          ? "bg-zinc-700 border-zinc-500 text-white"
                          : "bg-zinc-900 border-zinc-700 text-white/60 hover:border-zinc-500"
                      }`}
                    >
                      {lbl}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs text-white/50 uppercase tracking-wider">폰트</label>
                <div className="flex gap-1 mt-2 flex-wrap">
                  {[
                    ["tong", "통통체"],
                    ["gothic", "고딕"],
                  ].map(([val, lbl]) => (
                    <button
                      key={val}
                      onClick={() => setFont(val)}
                      className={`px-3 py-1 rounded-full text-xs border cursor-pointer transition-colors ${
                        font === val
                          ? "bg-zinc-700 border-zinc-500 text-white"
                          : "bg-zinc-900 border-zinc-700 text-white/60 hover:border-zinc-500"
                      }`}
                    >
                      {lbl}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </aside>
        ) : (
          <div className="border-r border-white/10 bg-zinc-950 p-3 flex justify-center">
            <button
              onClick={() => setShowStyle(true)}
              className="text-xs text-white/40 hover:text-white/80 cursor-pointer"
            >
              ▶
            </button>
          </div>
        )}

        <main className="flex flex-col items-center justify-center p-8 bg-[#1a0825] relative">
          <div className="relative h-[70vh] aspect-[9/16] bg-white rounded-lg shadow-2xl overflow-hidden">
            <div
              className={`absolute left-0 right-0 px-3 text-center break-keep ${positionClass} ${effectClass}`}
              style={{
                fontSize: `${fontSize}px`,
                color,
                fontWeight: fontWeightMap[font],
                textShadow: "0 1px 4px rgba(0,0,0,0.4)",
                lineHeight: 1.3,
              }}
            >
              미리보기
            </div>
          </div>

          <div className="w-full max-w-xl mt-6 flex items-center gap-3 px-4">
            <button className="w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center cursor-pointer">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
                <path d="M8 5v14l11-7z" />
              </svg>
            </button>
            <progress className="progress flex-1" value={12} max={35}></progress>
            <span className="text-xs text-white/70 tabular-nums">0:12 / 0:35</span>
          </div>
        </main>

        {showEmotion ? (
          <aside className="border-l border-white/10 bg-zinc-950 p-5 overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="font-medium">감정 설정</h2>
              <button
                onClick={() => setShowEmotion(false)}
                className="w-6 h-6 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-xs cursor-pointer"
              >
                ✕
              </button>
            </div>

            <div className="space-y-2">
              {Object.entries(emotionPresets).map(([key, p]) => (
                <button
                  key={key}
                  onClick={() => selectEmotion(key)}
                  className={`w-full flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors ${
                    emotion === key
                      ? "border-zinc-500 bg-zinc-800"
                      : "border-zinc-700 bg-zinc-900 hover:border-zinc-600"
                  }`}
                >
                  <div className="w-4 h-4 rounded-full flex-shrink-0" style={{ background: p.color }}></div>
                  <div className="text-left">
                    <div className="text-sm font-medium">{p.label}</div>
                    <div className="text-xs text-white/50 mt-0.5">{p.desc}</div>
                  </div>
                </button>
              ))}
            </div>
          </aside>
        ) : (
          <div className="border-l border-white/10 bg-zinc-950 p-3 flex justify-center">
            <button
              onClick={() => setShowEmotion(true)}
              className="text-xs text-white/40 hover:text-white/80 cursor-pointer"
            >
              ◀
            </button>
          </div>
        )}
      </div>

      <style jsx global>{`
        @keyframes shake {
          0%, 100% { transform: translateX(0); }
          25% { transform: translateX(-3px); }
          75% { transform: translateX(3px); }
        }
      `}</style>
    </div>
  );
}
