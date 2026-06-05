"use client";

import "./edit.css";
import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { uploadStore } from "../lib/upload-store";
import { API_BASE } from "../lib/api";

const EMOTION_COLORS = {
  Happy: "#F5C000",
  Angry: "#E03C3C",
  Sad: "#4A9FE0",
  Neutral: "#FFFFFF",
};

const DEFAULT_EMOTION_SETTINGS = {
  Happy: {
    fontSize: 23,
    position: "하단",
    effect: "바운스",
    font: "통통체",
  },
  Angry: {
    fontSize: 23,
    position: "하단",
    effect: "쉐이크",
    font: "각진체",
  },
  Sad: {
    fontSize: 23,
    position: "하단",
    effect: "페이드",
    font: "얇은체",
  },
  Neutral: {
    fontSize: 23,
    position: "하단",
    effect: "없음",
    font: "고딕",
  },
};

const EMOTIONS = [
  { name: "Happy", color: "#F5C000", desc: "통통체 · 23px" },
  { name: "Angry", color: "#E03C3C", desc: "각진체 · 23px" },
  { name: "Sad", color: "#4A9FE0", desc: "얇은체 · 23px" },
  { name: "Neutral", color: "#FFFFFF", desc: "고딕 · 23px" },
];

const EFFECT_CLASS = {
  바운스: "caption-bounce",
  페이드: "caption-fade",
  쉐이크: "caption-shake",
  없음: "",
};

const FONT_OPTIONS = ["통통체", "각진체", "얇은체", "고딕"];

const formatTime = (seconds = 0) => {
  const m = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const s = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");
  return `${m}:${s}`;
};

const getCaptionPositionStyle = (position) => {
  if (position === "상단") {
    return {
      top: "8%",
      bottom: "auto",
      transform: "translateX(-50%)",
    };
  }

  if (position === "중앙") {
    return {
      top: "50%",
      bottom: "auto",
      transform: "translate(-50%, -50%)",
    };
  }

  return {
    bottom: "8%",
    top: "auto",
    transform: "translateX(-50%)",
  };
};

const getCaptionFontFamily = (font) => {
  if (font === "통통체") return "'Arial Rounded MT Bold', sans-serif";
  if (font === "각진체") return "'Impact', sans-serif";
  if (font === "고딕") return "'Malgun Gothic', sans-serif";
  return "'Arial', sans-serif";
};

const makeSubtitlePayload = (segments, emotionSettings) => {
  return segments.map((segment) => {
    const emotion = segment.emotion ?? "Neutral";
    const setting = emotionSettings[emotion] ?? emotionSettings.Neutral;

    return {
      start: segment.start,
      end: segment.end,
      text: segment.text,
      emotion,

      // 백엔드에서 ASS 자막 스타일 만들 때 사용할 값
      color: EMOTION_COLORS[emotion] ?? "#FFFFFF",
      font: setting.font,
      fontSize: setting.fontSize,
      position: setting.position,
      effect: setting.effect,
    };
  });
};

export default function EditPage() {
  const router = useRouter();
  const videoRef = useRef(null);
  const scriptListRef = useRef(null);

  const [selectedEmotion, setSelectedEmotion] = useState("Happy");
  const [emotionSettings, setEmotionSettings] = useState(
    DEFAULT_EMOTION_SETTINGS,
  );
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [segments, setSegments] = useState(uploadStore.segments ?? []);
  const [duration, setDuration] = useState(
    uploadStore.videoInfo?.duration ?? 0,
  );
  const [isSubmitting, setIsSubmitting] = useState(false);

  const videoId = uploadStore.videoInfo?.video_id;
  const videoSrc = videoId ? `${API_BASE}/videos/${videoId}` : "";

  const currentSetting =
    emotionSettings[selectedEmotion] ?? emotionSettings.Neutral;

  const currentSegment =
    segments.find((seg) => currentTime >= seg.start && currentTime < seg.end) ??
    null;

  const captionEmotion = currentSegment?.emotion ?? selectedEmotion;
  const captionText = currentSegment?.text ?? "";
  const captionSetting =
    emotionSettings[captionEmotion] ?? emotionSettings.Neutral;

  const updateCurrentEmotionSetting = (key, value) => {
    setEmotionSettings((prev) => ({
      ...prev,
      [selectedEmotion]: {
        ...prev[selectedEmotion],
        [key]: value,
      },
    }));
  };

  const selectEmotion = (emotion) => {
    setSelectedEmotion(emotion);

    setSegments((prev) =>
      prev.map((seg, index) =>
        index === selectedIndex ? { ...seg, emotion } : seg,
      ),
    );
  };

  const handleTimeUpdate = () => {
    const video = videoRef.current;
    if (!video) return;

    const time = video.currentTime;
    setCurrentTime(time);

    if (segments.length === 0) return;

    let idx = 0;

    for (let i = 0; i < segments.length; i++) {
      if (segments[i].start <= time) {
        idx = i;
      } else {
        break;
      }
    }

    setSelectedIndex((prev) => {
      if (prev !== idx) {
        setSelectedEmotion(segments[idx]?.emotion ?? "Neutral");
        return idx;
      }

      return prev;
    });
  };

  const handleLoadedMetadata = () => {
    const video = videoRef.current;
    if (!video) return;

    setDuration(video.duration || uploadStore.videoInfo?.duration || 0);
  };

  const togglePlay = () => {
    const video = videoRef.current;
    if (!video) return;

    if (isPlaying) {
      video.pause();
    } else {
      video.play();
    }

    setIsPlaying((prev) => !prev);
  };

  const handleProgressClick = (event) => {
    const video = videoRef.current;
    if (!video || !duration) return;

    const rect = event.currentTarget.getBoundingClientRect();
    const ratio = (event.clientX - rect.left) / rect.width;

    video.currentTime = ratio * duration;
  };

  const seekToSegment = (index, start) => {
    setSelectedIndex(index);
    setCurrentTime(start);
    setSelectedEmotion(segments[index]?.emotion ?? "Neutral");

    const video = videoRef.current;
    if (!video) return;

    video.pause();
    video.currentTime = start;
    setIsPlaying(false);
  };

  const scrollScript = (direction) => {
    scriptListRef.current?.scrollBy({
      top: direction * 80,
      behavior: "smooth",
    });
  };

  const handleCompleteEdit = async () => {
    if (isSubmitting) return;

    const subtitleData = makeSubtitlePayload(segments, emotionSettings);

    const finalPayload = {
      video_id: videoId,
      subtitles: subtitleData,
    };

    uploadStore.finalPayload = finalPayload;

    console.log("백엔드로 보낼 최종 데이터:", finalPayload);

    try {
      setIsSubmitting(true);

      console.log(JSON.stringify(finalPayload));

      const response = await fetch(`${API_BASE}/process`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(finalPayload),
      });

      if (!response.ok) {
        throw new Error("최종 영상 생성 요청 실패");
      }

      const result = await response.json();

      // 백엔드에서 반환한 다운로드 결과 저장
      uploadStore.finalResult = result;

      console.log("백엔드에서 받은 다운로드 결과:", result);

      router.push("/download");
    } catch (error) {
      console.error("편집 완료 처리 중 오류:", error);
      alert("최종 영상 생성 중 오류가 발생했습니다.");
    } finally {
      setIsSubmitting(false);
    }
  };

  useEffect(() => {
    const activeEmotion = segments[selectedIndex]?.emotion ?? "Neutral";
    setSelectedEmotion(activeEmotion);
  }, [selectedIndex, segments]);

  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.code === "Space" && event.target === document.body) {
        event.preventDefault();
        togglePlay();
      }
    };

    document.addEventListener("keydown", handleKeyDown);

    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [isPlaying]);

  return (
    <div className="edit-container">
      <header className="edit-header">
        <Link href="/" className="logo-link">
          <h1 className="logo-text">VIBE-WRITER</h1>
        </Link>

        <p className="service-text">AI 감정 기반 숏폼 자막 자동 생성 서비스</p>
      </header>

      <div className="edit-body">
        <aside className="edit-left">
          <div className="panel-header-row">
            <span className="panel-title">스타일 설정</span>
            <button type="button" className="panel-close-btn">
              ✕
            </button>
          </div>

          <div className="style-settings-box">
            <div className="setting-group">
              <div className="setting-label-row">
                <span className="setting-label">글자 크기</span>
                <span className="font-size-value">
                  {currentSetting.fontSize}px
                </span>
              </div>

              <input
                type="range"
                min={10}
                max={100}
                value={currentSetting.fontSize}
                onChange={(e) =>
                  updateCurrentEmotionSetting(
                    "fontSize",
                    Number(e.target.value),
                  )
                }
                className="font-size-slider"
              />
            </div>

            <div className="setting-group">
              <span className="setting-label">위치</span>

              <div className="pill-group">
                {["하단", "중앙", "상단"].map((item) => (
                  <button
                    type="button"
                    key={item}
                    className={`pill-btn${
                      currentSetting.position === item ? " selected" : ""
                    }`}
                    onClick={() =>
                      updateCurrentEmotionSetting("position", item)
                    }
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>

            <div className="setting-group">
              <span className="setting-label">효과</span>

              <div className="pill-group">
                {["바운스", "페이드", "쉐이크", "없음"].map((item) => (
                  <button
                    type="button"
                    key={item}
                    className={`pill-btn${
                      currentSetting.effect === item ? " selected" : ""
                    }`}
                    onClick={() => updateCurrentEmotionSetting("effect", item)}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>

            <div className="setting-group">
              <span className="setting-label">폰트</span>

              <div className="pill-group">
                {FONT_OPTIONS.map((item) => (
                  <button
                    type="button"
                    key={item}
                    className={`pill-btn${
                      currentSetting.font === item ? " selected" : ""
                    }`}
                    onClick={() => updateCurrentEmotionSetting("font", item)}
                  >
                    {item}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="panel-header-row">
            <span className="panel-title">감정 설정</span>
          </div>

          <div className="emotion-list">
            {EMOTIONS.map((emotion) => (
              <button
                type="button"
                key={emotion.name}
                className={`emotion-item${
                  selectedEmotion === emotion.name ? " active" : ""
                }`}
                onClick={() => selectEmotion(emotion.name)}
              >
                <span
                  className="emotion-dot"
                  style={{ backgroundColor: emotion.color }}
                />
                <span className="emotion-name">{emotion.name}</span>
                <span className="emotion-desc">{emotion.desc}</span>
              </button>
            ))}
          </div>
        </aside>

        <main className="edit-center">
          <div className="video-area">
            <div className="video-wrapper">
              {videoSrc ? (
                <video
                  ref={videoRef}
                  src={videoSrc}
                  className="video-frame"
                  onLoadedMetadata={handleLoadedMetadata}
                  onTimeUpdate={handleTimeUpdate}
                  onEnded={() => setIsPlaying(false)}
                />
              ) : (
                <div className="video-frame empty-video">
                  영상을 불러오는 중입니다
                </div>
              )}

              {captionText && (
                <div
                  className={`caption-preview ${
                    EFFECT_CLASS[captionSetting.effect]
                  }`}
                  style={{
                    color: EMOTION_COLORS[captionEmotion] ?? "#FFFFFF",
                    fontSize: `${captionSetting.fontSize}px`,
                    fontFamily: getCaptionFontFamily(captionSetting.font),
                    fontWeight: captionSetting.font === "얇은체" ? 400 : 900,
                    ...getCaptionPositionStyle(captionSetting.position),
                  }}
                >
                  {captionText}
                </div>
              )}
            </div>
          </div>

          <div className="video-controls">
            <button
              type="button"
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

        <aside className="edit-right">
          <div className="script-title">스크립트</div>

          <button
            type="button"
            className="scroll-arrow"
            onClick={() => scrollScript(-1)}
          >
            ▲
          </button>

          <div className="script-list" ref={scriptListRef}>
            {segments.length === 0 ? (
              <div className="script-empty-message">
                분석된 자막이 없습니다.
              </div>
            ) : (
              segments.map((segment, index) => (
                <button
                  type="button"
                  key={index}
                  className={`script-item${
                    selectedIndex === index ? " selected-script" : ""
                  }`}
                  onClick={() => seekToSegment(index, segment.start)}
                >
                  <span className="script-time">
                    {formatTime(segment.start)}
                  </span>

                  <div className="script-info">
                    <span className="script-text">{segment.text}</span>

                    <span
                      className="script-emotion"
                      style={{
                        color: EMOTION_COLORS[segment.emotion] ?? "#FFFFFF",
                      }}
                    >
                      {segment.emotion ?? "Neutral"}
                    </span>
                  </div>
                </button>
              ))
            )}
          </div>

          <button
            type="button"
            className="scroll-arrow"
            onClick={() => scrollScript(1)}
          >
            ▼
          </button>

          <div className="script-footer">
            <button
              type="button"
              className="done-btn"
              onClick={handleCompleteEdit}
              disabled={isSubmitting}
            >
              {isSubmitting ? "처리 중..." : "편집 완료"}
            </button>
          </div>
        </aside>
      </div>
    </div>
  );
}
