import os
import shutil
import subprocess
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_video_duration(file_path: str) -> float:
    """ffprobe로 영상 길이 추출 (실패 시 0)"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            capture_output=True, text=True, timeout=10
        )
        return round(float(result.stdout.strip()), 2)
    except Exception:
        return 0.0


@router.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    # 형식 체크
    if not video.filename or not video.filename.lower().endswith((".mp4", ".mov")):
        raise HTTPException(400, detail="INVALID_FORMAT")

    # video_id 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_id = f"vid_{timestamp}"
    file_path = os.path.join(UPLOAD_DIR, f"{video_id}.mp4")

    # 파일 저장
    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(video.file, f)
    except Exception:
        raise HTTPException(500, detail="SAVE_FAILED")

    # 메타데이터
    size_bytes = os.path.getsize(file_path)
    size_mb = round(size_bytes / (1024 * 1024), 1)

    # 60초/50MB 초과 체크
    if size_mb > 50:
        os.remove(file_path)
        raise HTTPException(400, detail="FILE_TOO_LARGE")

    duration = get_video_duration(file_path)
    if duration > 60:
        os.remove(file_path)
        raise HTTPException(400, detail="FILE_TOO_LARGE")

    return {
        "video_id": video_id,
        "duration": duration,
        "filename": video.filename,
        "size_mb": size_mb,
    }