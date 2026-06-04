import os
import sys
import subprocess
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Union

router = APIRouter()

UPLOAD_DIR = Path(os.path.dirname(__file__)) / "uploads"
OUTPUT_VIDEO_DIR = Path(os.path.dirname(__file__)) / "output" / "videos"
OUTPUT_ASS_DIR = Path(os.path.dirname(__file__)) / "output" / "subtitles"
OUTPUT_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_ASS_DIR.mkdir(parents=True, exist_ok=True)


# ── 매핑 테이블 ────────────────────────────
# 한글 폰트명 → 시스템 설치된 폰트명 (개발은 일단 맑은 고딕으로 통일, 추후 교체 가능)
FONT_MAP = {
    "통통체": "Malgun Gothic",
    "각진체": "Malgun Gothic",
    "얇은체": "Malgun Gothic",
    "고딕": "Malgun Gothic",
}

# 한글 위치 → ASS Alignment (numpad 1~9)
POSITION_MAP = {
    "상단": 8,    # top center
    "중앙": 5,    # middle center
    "하단": 2,    # bottom center
    "top": 8, "middle": 5, "bottom": 2, "center": 5,
}


# ── Pydantic 스키마 ────────────────────────
class Segment(BaseModel):
    start: float
    end: float
    text: str
    emotion: str
    color: Optional[str] = "#FFFFFF"
    font: Optional[str] = "고딕"
    fontSize: Optional[int] = 50
    position: Optional[str] = "하단"


class ProcessRequest(BaseModel):
    video_id: str
    segments: list[Segment]


# ── 유틸 함수 ──────────────────────────────
def hex_to_ass_color(hex_color: str) -> str:
    """#RRGGBB → &H00BBGGRR (ASS는 BGR 순서)"""
    h = hex_color.lstrip("#").upper()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return "&H00FFFFFF"
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}"


def to_ass_time(sec: float) -> str:
    """0.0 → 0:00:00.00 (센티초)"""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def build_ass(segments: list[Segment]) -> str:
    """Segment 리스트 → ASS 파일 텍스트"""
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1080\n"
        "PlayResY: 1920\n"
        "WrapStyle: 0\n"
        "ScaledBorderAndShadow: yes\n"
        "\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Default,Malgun Gothic,50,&H00FFFFFF,&H000000FF,&H00000000,"
        "&H80000000,0,0,0,0,100,100,0,0,1,2,1,2,40,40,80,1\n"
        "\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
        "Effect, Text\n"
    )

    lines = [header]
    for seg in segments:
        start_t = to_ass_time(seg.start)
        end_t = to_ass_time(seg.end)
        color_ass = hex_to_ass_color(seg.color or "#FFFFFF")
        font_name = FONT_MAP.get(seg.font or "고딕", "Malgun Gothic")
        alignment = POSITION_MAP.get(seg.position or "하단", 2)
        font_size = seg.fontSize or 50

        # 인라인 오버라이드 태그로 segment별 스타일 적용
        override = (
            f"{{\\an{alignment}"
            f"\\fn{font_name}"
            f"\\fs{font_size}"
            f"\\c{color_ass}"
            f"}}"
        )
        # 줄바꿈은 \\N (ASS 표준)
        text = seg.text.replace("\n", "\\N").replace("\r", "")
        lines.append(
            f"Dialogue: 0,{start_t},{end_t},Default,,0,0,0,,{override}{text}"
        )

    return "\n".join(lines) + "\n"


# ── 메인 엔드포인트 ────────────────────────
@router.post("/process")
async def process_video(req: ProcessRequest):
    video_path = UPLOAD_DIR / f"{req.video_id}.mp4"
    if not video_path.exists():
        raise HTTPException(404, detail="VIDEO_NOT_FOUND")

    output_video = OUTPUT_VIDEO_DIR / f"{req.video_id}.mp4"
    output_ass = OUTPUT_ASS_DIR / f"{req.video_id}.ass"

    try:
        # ① ASS 파일 생성
        ass_text = build_ass(req.segments)
        output_ass.write_text(ass_text, encoding="utf-8")

        # ② ffmpeg로 ASS + MP4 합성
        # subtitles 필터는 경로에 콜론/슬래시 escape 까다로움 → cwd 지정으로 우회
        ass_filename = output_ass.name
        cmd = [
            "ffmpeg", "-y",
            "-i", str(video_path.resolve()),
            "-vf", f"subtitles={ass_filename}",
            "-c:a", "copy",
            str(output_video.resolve()),
        ]
        result = subprocess.run(
            cmd,
            cwd=str(output_ass.parent.resolve()),
            capture_output=True,
            text=True,
            timeout=300,
        )

        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {result.stderr[-500:]}")

        return {"success": True, "video_id": req.video_id}

    except Exception as e:
        # 실패 마커
        (OUTPUT_VIDEO_DIR / f"{req.video_id}.failed").touch()
        raise HTTPException(500, detail=f"PROCESS_FAILED: {str(e)}")