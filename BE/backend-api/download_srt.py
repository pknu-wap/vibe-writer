import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

SRT_DIR = os.path.join(os.path.dirname(__file__), "output", "subtitles")


@router.get("/download-srt")
async def download_srt(video_id: str):
    if not video_id or ".." in video_id or "/" in video_id or "\\" in video_id:
        raise HTTPException(status_code=400, detail="Invalid video_id")

    file_path = os.path.join(SRT_DIR, f"{video_id}.srt")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="SRT_NOT_FOUND")

    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename=f"vibe_writer_{video_id}.srt",
    )
