import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

VIDEO_DIR = os.path.join(os.path.dirname(__file__), "output", "videos")


@router.get("/download")
async def download_video(video_id: str):
    if not video_id:
        raise HTTPException(status_code=422, detail="video_id is required")

    failed_marker = os.path.join(VIDEO_DIR, f"{video_id}.failed")
    if os.path.exists(failed_marker):
        raise HTTPException(status_code=500, detail="RENDER_FAILED")

    file_path = os.path.join(VIDEO_DIR, f"{video_id}.mp4")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="VIDEO_NOT_READY")

    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=f"vibe_writer_{video_id}.mp4",
    )
