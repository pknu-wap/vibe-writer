import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

# 1. 가이드라인에 따른 절대 경로 설정
SRT_DIR = os.path.join(os.path.dirname(__file__), "output", "subtitles")

# 2. [추가] 가이드라인 요구사항: 자막 폴더가 없으면 자동으로 생성
os.makedirs(SRT_DIR, exist_ok=True)


@router.get("/download-srt")
async def download_srt(video_id: str):
    # 상위 디렉토리 접근 차단 검증
    if not video_id or ".." in video_id or "/" in video_id or "\\" in video_id:
        raise HTTPException(status_code=400, detail="Invalid video_id")

    # 실제 SRT 자막 파일 확인
    file_path = os.path.join(SRT_DIR, f"{video_id}.srt")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="SRT_NOT_FOUND")

    # 자막 파일 다운로드 응답
    return FileResponse(
        path=file_path,
        media_type="application/x-subrip",
        filename=f"vibe_writer_{video_id}.srt",
    )