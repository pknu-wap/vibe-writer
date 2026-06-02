import os
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

# upload.py와 같은 폴더, 같은 이름 규칙으로 통일
UPLOAD_DIR = Path(os.path.dirname(__file__)) / "uploads"


@router.get("/videos/{video_id}")
async def stream_video(video_id: str):
    if "/" in video_id or "\\" in video_id or ".." in video_id:
        raise HTTPException(status_code=400, detail="Invalid video_id")

    video_path = UPLOAD_DIR / f"{video_id}.mp4"

    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    return FileResponse(path=str(video_path), media_type="video/mp4")