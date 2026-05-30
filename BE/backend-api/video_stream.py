from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

# ⚠️ 우하진과 실제 저장 경로·파일명 합의 필요
VIDEOS_DIR = Path("out/videos")


@router.get("/videos/{video_id}")
async def stream_video(video_id: str):
    # 경로 조작 방지
    if "/" in video_id or "\\" in video_id or ".." in video_id:
        raise HTTPException(status_code=400, detail="Invalid video_id")

    # 파일 경로 구성
    video_path = VIDEOS_DIR / f"{video_id}.mp4"

    # 파일 없으면 404
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")

    # FileResponse 반환 (Range 요청 자동 지원 → seek 가능)
    return FileResponse(path=video_path, media_type="video/mp4")