import os
import sys
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")

# AI 모듈 경로 추가
AI_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "AI"))
if AI_PATH not in sys.path:
    sys.path.insert(0, AI_PATH)


class AnalyzeRequest(BaseModel):
    video_id: str


@router.post("/analyze")
async def analyze_video(req: AnalyzeRequest):
    # 파일 존재 확인
    video_path = os.path.join(UPLOAD_DIR, f"{req.video_id}.mp4")
    if not os.path.exists(video_path):
        raise HTTPException(404, detail="VIDEO_NOT_FOUND")

    # AI 함수 호출 (느림 — 1분 영상 기준 15~30초)
    try:
        from stt import analyze_stt
        segments = analyze_stt(video_path)
    except Exception as e:
        raise HTTPException(500, detail=f"STT_FAILED: {str(e)}")

    return {
        "video_id": req.video_id,
        "segments": segments,
    }