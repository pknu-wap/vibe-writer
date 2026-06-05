import os
import sys
import subprocess
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

router = APIRouter()

UPLOAD_DIR = Path(os.path.dirname(__file__)) / "uploads"
OUTPUT_VIDEO_DIR = Path(os.path.dirname(__file__)) / "output" / "videos"
OUTPUT_ASS_DIR = Path(os.path.dirname(__file__)) / "output" / "subtitles"
OUTPUT_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_ASS_DIR.mkdir(parents=True, exist_ok=True)

# FE 미리보기 px값을 ASS 좌표(PlayResY=1920)로 키울 배수
FONT_SIZE_SCALE = 4

# 위치별 MarginV (ASS 좌표계 1920 기준)
POSITION_MARGIN_V = {
    "상단": 120,    # 위에서 약간 떨어진 곳
    "중앙": 0,      # 정중앙
    "하단": 500,    # 아래에서 좀 떨어진 곳
    "top": 120, "middle": 0, "bottom": 500,
}

POSITION_ALIGNMENT = {
    "상단": 8,
    "중앙": 5,
    "하단": 2,
    "top": 8, "middle": 5, "bottom": 2, "center": 5,
}

FONT_MAP = {
    "통통체": "NanumGothic",
    "각진체": "NanumGothic",
    "얇은체": "NanumGothic",
    "고딕": "NanumGothic",
}


class Segment(BaseModel):
    start: float
    end: float
    text: str
    emotion: str
    color: Optional[str] = "#FFFFFF"
    font: Optional[str] = "고딕"
    fontSize: Optional[int] = 50
    position: Optional[str] = "하단"


# ⭐ segments 또는 subtitles 둘 다 받아들임 (FE 코드 어느 쪽이어도 OK)
class ProcessRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    video_id: str
    subtitles: list[Segment] = Field(default_factory=list, alias="segments")


def hex_to_ass_color(hex_color: str) -> str:
    h = hex_color.lstrip("#").upper()
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return "&H00FFFFFF"
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H00{b}{g}{r}"


def to_ass_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def build_ass(segments):
    header = (
        "[Script Info]\n"
        "ScriptType: v4.00+\n"
        "PlayResX: 1080\n"
        "PlayResY: 1920\n"
        "WrapStyle: 0\n"
        "ScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, "
        "OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, "
        "ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
        "Alignment, MarginL, MarginR, MarginV, Encoding\n"
        "Style: Default,NanumGothic,80,&H00FFFFFF,&H000000FF,&H00000000,"
        "&H80000000,0,0,0,0,100,100,0,0,1,3,1,2,40,40,200,1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, "
        "Effect, Text\n"
    )

    lines = [header]
    for seg in segments:
        start_t = to_ass_time(seg.start)
        end_t = to_ass_time(seg.end)
        color_ass = hex_to_ass_color(seg.color or "#FFFFFF")
        font_name = FONT_MAP.get(seg.font or "고딕", "NanumGothic")
        pos_key = seg.position or "하단"
        alignment = POSITION_ALIGNMENT.get(pos_key, 2)
        margin_v = POSITION_MARGIN_V.get(pos_key, 200)
        font_size = (seg.fontSize or 20) * FONT_SIZE_SCALE

        # 인라인으로 alignment/font/size/color/marginV 모두 오버라이드
        # MarginV는 \pos 또는 별도 dialogue MarginV 필드로 제어 가능
        override = (
            f"{{\\an{alignment}\\fn{font_name}\\fs{font_size}\\c{color_ass}}}"
        )
        text = seg.text.replace("\n", "\\N").replace("\r", "")

        # Dialogue 라인의 MarginV 필드 (8번째)를 위치별로 다르게
        lines.append(
            f"Dialogue: 0,{start_t},{end_t},Default,,0,0,{margin_v},,{override}{text}"
        )

    return "\n".join(lines) + "\n"


@router.post("/process")
async def process_video(req: ProcessRequest):
    video_path = UPLOAD_DIR / f"{req.video_id}.mp4"
    if not video_path.exists():
        raise HTTPException(404, detail="VIDEO_NOT_FOUND")

    output_video = OUTPUT_VIDEO_DIR / f"{req.video_id}.mp4"
    output_ass = OUTPUT_ASS_DIR / f"{req.video_id}.ass"

    try:
        ass_text = build_ass(req.subtitles)
        output_ass.write_text(ass_text, encoding="utf-8")

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
        (OUTPUT_VIDEO_DIR / f"{req.video_id}.failed").touch()
        raise HTTPException(500, detail=f"PROCESS_FAILED: {str(e)}")
