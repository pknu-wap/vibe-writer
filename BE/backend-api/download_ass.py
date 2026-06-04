import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

ASS_DIR = os.path.join(os.path.dirname(__file__), "output", "subtitles")
os.makedirs(ASS_DIR, exist_ok=True)


@router.get("/download-ass")
async def download_ass(video_id: str):
    if "/" in video_id or "\\" in video_id or ".." in video_id:
        raise HTTPException(400, detail="Invalid video_id")

    ass_path = os.path.join(ASS_DIR, f"{video_id}.ass")
    if not os.path.exists(ass_path):
        raise HTTPException(404, detail="SUBTITLE_NOT_FOUND")

    return FileResponse(
        path=ass_path,
        media_type="text/plain; charset=utf-8",
        filename=f"vibe_writer_{video_id}.ass",
    )