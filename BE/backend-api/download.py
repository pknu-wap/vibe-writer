import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

# 1. 가이드라인에 따른 절대 경로 설정
VIDEO_DIR = os.path.join(os.path.dirname(__file__), "output", "videos")

# 2. [추가] 가이드라인 요구사항: 폴더가 없으면 자동으로 생성 (안전장치)
os.makedirs(VIDEO_DIR, exist_ok=True)


@router.get("/download")
async def download_video(video_id: str):
    # 상위 디렉토리 접근 차단 등 보안 검증 (잘 작성하셨습니다!)
    if not video_id or ".." in video_id or "/" in video_id or "\\" in video_id:
        raise HTTPException(status_code=400, detail="Invalid video_id")

    # 실패 마커 확인
    failed_marker = os.path.join(VIDEO_DIR, f"{video_id}.failed")
    if os.path.exists(failed_marker):
        raise HTTPException(status_code=500, detail="RENDER_FAILED")

    # 실제 MP4 파일 확인
    file_path = os.path.join(VIDEO_DIR, f"{video_id}.mp4")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="VIDEO_NOT_READY")

    # 파일 다운로드 응답
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=f"vibe_writer_{video_id}.mp4",
    )