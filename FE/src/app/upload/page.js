"use client";

import { useRef, useState } from "react";
import { useRouter } from "next/navigation";
import TopNav from "../components/top-nav";
import { uploadStore } from "../lib/upload-store";
import "./upload.css";

export default function UploadPage() {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const router = useRouter();

  const handleFile = (file) => {
    if (!file) return;

    const form = new FormData();
    form.append("video", file);
    uploadStore.promise = fetch("/api/upload", {
      method: "POST",
      body: form,
    }).then((res) => res.json());

    router.push("/loading");
  };

  const handleDebug = () => {
    uploadStore.promise = fetch("/api/upload", { method: "POST" })
      .then((res) => res.json());
    router.push("/loading");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    handleFile(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleInputChange = (e) => {
    handleFile(e.target.files?.[0]);
  };

  return (
    <div className="upload-container">
      <TopNav />

      <div className="upload-content">
        <h1 className="upload-title">VIBE - WRITER</h1>

        <div
          className={`upload-card-wrapper${isDragging ? " dragging" : ""}`}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <div className="upload-card">
            <div className="upload-icon-circle">
              <svg width="60" height="60" viewBox="0 0 60 60" fill="none">
                <path
                  d="M30 10V38M30 38L20 28M30 38L40 28"
                  stroke="white"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                <path
                  d="M14 46H46"
                  stroke="white"
                  strokeWidth="3.5"
                  strokeLinecap="round"
                />
              </svg>
            </div>

            <p className="upload-desc">영상을 여기에 첨부 해 주세요.</p>
            <p className="upload-hint">새로형(9:16), 60초 이내, MP4</p>

            <input
              ref={inputRef}
              type="file"
              accept="video/mp4"
              className="upload-input-hidden"
              onChange={handleInputChange}
            />
            <button
              className="upload-select-btn"
              onClick={() => inputRef.current?.click()}
            >
              영상 선택하기
            </button>
          </div>
        </div>

        <button className="debug-btn" onClick={handleDebug}>
          DEBUG
        </button>
      </div>
    </div>
  );
}
