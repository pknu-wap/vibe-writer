"use client";

import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import TopNav from "../components/top-nav";
import { uploadStore } from "../lib/upload-store";
import "./edit.css";

const EMOTION_COLORS = {
  Happy: "#F5C000",
  Angry: "#E03C3C",
  Sad: "#4A9FE0",
  Neutral: "#888888",
};

const formatTime = (seconds) => {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const s = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");
  return `${m}:${s}`;
};

const EMOTIONS = [
  { name: "Happy", color: "#F5C000", desc: "통통체 · 65px" },
  { name: "Angry", color: "#E03C3C", desc: "각진체 · 70px" },
  { name: "Sad", color: "#4A9FE0", desc: "얇은체 · 45px" },
  { name: "Neutral", color: "#888888", desc: "고딕 · 50px" },
];

export default function EditPage() {
  const [fontSize, setFontSize] = useState(50);
  const [position, setPosition] = useState("하단");
  const [effect, setEffect] = useState("바운스");
  const [font, setFont] = useState("통둥체");
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const videoRef = useRef(null);
  const scriptListRef = useRef(null);
  const router = useRouter();

  const [segments, setSegments] = useState(uploadStore.segments ?? []);
  const duration = uploadStore.videoInfo?.duration ?? 0;
  const videoId = uploadStore.videoInfo?.video_id;
  const videoSrc = videoId ? `/api/video/${videoId}` : null;

  const togglePlay = () => {
    const video = videoRef.current;
    if (!video) return;
    isPlaying ? video.pause() : video.play();
    setIsPlaying((p) => !p);
  };

  const handleTimeUpdate = () => {
    const time = videoRef.current?.currentTime ?? 0;
    setCurrentTime(time);

    if (segments.length === 0) return;
    let idx = 0;
    for (let i = 0; i < segments.length; i++) {
      if (segments[i].start <= time) idx = i;
      else break;
    }
    setSelectedIndex((prev) => (prev !== idx ? idx : prev));
  };

  const handleProgressClick = (e) => {
    const video = videoRef.current;
    if (!video) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const ratio = (e.clientX - rect.left) / rect.width;
    video.currentTime = ratio * duration;
  };

  const seekToSegment = (index, start) => {
    const video = videoRef.current;
    if (!video) return;
    video.pause();
    video.currentTime = start;
    setIsPlaying(false);
    setSelectedIndex(index);
  };

  const changeEmotion = (emotion) => {
    setSegments((prev) =>
      prev.map((s, i) => (i === selectedIndex ? { ...s, emotion } : s)),
    );
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.code === "Space" && e.target === document.body) {
        e.preventDefault();
        togglePlay();
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isPlaying]);

  const scrollScript = (dir) => {
    scriptListRef.current?.scrollBy({ top: dir * 80, behavior: "smooth" });
  };

  return (
    <div className="edit-container">
      <TopNav />

      <div className="edit-body">
        {/* ── Left panel ── */}
        <aside className="edit-left">
          <div className="panel-header-row">
            <span className="panel-title">스타일 설정</span>
            <button className="panel-close-btn">✕</button>
          </div>

          <div className="style-settings-box">
            <div className="setting-group">
              <label className="setting-label">글자 크기</label>
              <input
                type="range"
                min={10}
                max={100}
                value={fontSize}
                onChange={(e) => setFontSize(+e.target.value)}
                className="font-size-slider"
              />
            </div>

            <div className="setting-group">
              <label className="setting-label">위치</label>
              <div className="pill-group">
                {["하단", "중양", "상단"].map((v) => (
                  <button
                    key={v}
                    className={`pill-btn${position === v ? " selected" : ""}`}
                    onClick={() => setPosition(v)}
                  >
                    {v}
                  </button>
                ))}
              </div>
            </div>

            <div className="setting-group">
              <label className="setting-label">효과</label>
              <div className="pill-group">
                {["바운스", "페이드", "쉐이크", "없음"].map((v) => (
                  <button
                    key={v}
                    className={`pill-btn${effect === v ? " selected" : ""}`}
                    onClick={() => setEffect(v)}
                  >
                    {v}
                  </button>
                ))}
              </div>
            </div>

            <div className="setting-group">
              <label className="setting-label">폰트</label>
              <div className="pill-group">
                {["통통체", "고딕"].map((v) => (
                  <button
                    key={v}
                    className={`pill-btn${font === v ? " selected" : ""}`}
                    onClick={() => setFont(v)}
                  >
                    {v}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="panel-header-row">
            <span className="panel-title">감정 설정</span>
          </div>

          <div className="emotion-list">
            {EMOTIONS.map((em) => (
              <div
                key={em.name}
                className="emotion-item"
                onClick={() => changeEmotion(em.name)}
              >
                <span
                  className="emotion-dot"
                  style={{ background: em.color }}
                />
                <span className="emotion-name">{em.name}</span>
                <span className="emotion-desc">{em.desc}</span>
              </div>
            ))}
          </div>
        </aside>

        {/* ── Center video ── */}
        <main className="edit-center">
          <div className="video-area">
            <video
              ref={videoRef}
              src={videoSrc}
              className="video-frame"
              onTimeUpdate={handleTimeUpdate}
              onEnded={() => setIsPlaying(false)}
            />
          </div>

          <div className="video-controls">
            <button
              className="play-btn"
              onClick={togglePlay}
              aria-label={isPlaying ? "일시정지" : "재생"}
            >
              {isPlaying ? (
                <svg width="20" height="20" viewBox="0 0 20 20" fill="white">
                  <rect x="3" y="2" width="5" height="16" rx="1" />
                  <rect x="12" y="2" width="5" height="16" rx="1" />
                </svg>
              ) : (
                <svg width="20" height="20" viewBox="0 0 20 20" fill="white">
                  <path d="M4 3l13 7-13 7V3z" />
                </svg>
              )}
            </button>
            <div className="progress-track" onClick={handleProgressClick}>
              <div
                className="progress-fill"
                style={{
                  width: duration ? `${(currentTime / duration) * 100}%` : "0%",
                }}
              />
            </div>
            <span className="time-label">
              {formatTime(currentTime)} / {formatTime(duration)}
            </span>
          </div>
        </main>

        {/* ── Right script panel ── */}
        <aside className="edit-right">
          <div className="script-title">스크립트</div>
          <button className="scroll-arrow" onClick={() => scrollScript(-1)}>
            ▲
          </button>
          <div className="script-list" ref={scriptListRef}>
            {segments.map((s, i) => (
              <div
                key={i}
                className="script-item"
                style={
                  selectedIndex === i
                    ? {
                        background: "#1e3a6e",
                        borderColor: "rgba(100, 160, 255, 0.7)",
                        boxShadow: "0 0 8px rgba(80, 140, 255, 0.25)",
                      }
                    : {}
                }
                onClick={() => seekToSegment(i, s.start)}
              >
                <span className="script-time">{formatTime(s.start)}</span>
                <div className="script-info">
                  <span className="script-text">{s.text}</span>
                  <span
                    className="script-emotion"
                    style={{ color: EMOTION_COLORS[s.emotion] ?? "#fff" }}
                  >
                    {s.emotion}
                  </span>
                </div>
              </div>
            ))}
          </div>
          <button className="scroll-arrow" onClick={() => scrollScript(1)}>
            ▼
          </button>

          <div className="script-footer">
            <button
              className="done-btn"
              onClick={() => router.push("/loading-final")}
            >
              편집 완료
            </button>
          </div>
        </aside>
      </div>
    </div>
  );
}
