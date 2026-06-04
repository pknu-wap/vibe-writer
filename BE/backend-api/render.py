import os
import sys
import subprocess
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

UPLOAD_DIR = Path(os.path.dirname(__file__)) / "uploads"
OUTPUT_VIDEO_DIR = Path(os.path.dirname(__file__)) / "output" / "videos"
OUTPUT_SRT_DIR = Path(os.path.dirname(__file__)) / "output" / "subtitles"
OUTPUT_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_SRT_DIR.mkdir(parents=True, exist_ok=True)

# BE 폴더 import 경로 추가
BE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
if BE_PATH not in sys.path:
    sys.path.insert(0, BE_PATH)


class Segment(BaseModel):
    text: str
    start: float
    end: float
    emotion: str


class RenderRequest(BaseModel):
    video_id: str
    segments: list[Segment]


def _to_srt_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec - int(sec)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def _build_srt(segments: list) -> str:
    lines = []
    for i, seg in enumerate(segments, 1):
        lines.append(str(i))
        lines.append(f"{_to_srt_time(seg.start)} --> {_to_srt_time(seg.end)}")
        lines.append(seg.text)
        lines.append("")
    return "\n".join(lines)


@router.post("/render")
async def render_video(req: RenderRequest):
    video_path = UPLOAD_DIR / f"{req.video_id}.mp4"
    if not video_path.exists():
        raise HTTPException(404, detail="VIDEO_NOT_FOUND")

    output_video = OUTPUT_VIDEO_DIR / f"{req.video_id}.mp4"
    output_srt = OUTPUT_SRT_DIR / f"{req.video_id}.srt"
    frames_dir = UPLOAD_DIR / f"frames_{req.video_id}"
    frames_dir.mkdir(exist_ok=True)

    try:
        from video_utils import render_all_frames, extract_audio
        from export_utils import merge_video

        # segments를 dict 리스트로 변환
        segs = [
            {"text": s.text, "start": s.start, "end": s.end, "emotion": s.emotion}
            for s in req.segments
        ]

        # ① 자막 입힌 프레임 생성
        render_all_frames(str(video_path), segs, str(frames_dir))

        # ② 오디오 추출
        audio_path = extract_audio(str(video_path))

        # ③ 최종 합성
        merge_video(str(frames_dir), audio_path, str(output_video))

        # ④ SRT 파일 저장
        srt_text = _build_srt(req.segments)
        output_srt.write_text(srt_text, encoding="utf-8")

        return {"success": True, "video_id": req.video_id}

    except Exception as e:
        # 실패 마커 생성 (download.py가 RENDER_FAILED 응답)
        failed_marker = OUTPUT_VIDEO_DIR / f"{req.video_id}.failed"
        failed_marker.touch()
        raise HTTPException(500, detail=f"RENDER_FAILED: {str(e)}")