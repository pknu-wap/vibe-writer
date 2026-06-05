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

POSITION_MARGIN_V = {
    "상단": 120,
    "중앙": 0,
    "하단": 400,
    "top": 120, "middle": 0, "bottom": 400,
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

# 감정별 효과 → ASS 애니메이션 오버라이드 태그
EFFECT_OVERRIDE = {
    # 통통튀는 효과 (Happy): 살짝 페이드인 + 살짝 커졌다 돌아옴
    "바운스": r"\fad(150,0)\t(0,200,\fscx115\fscy115)\t(200,400,\fscx100\fscy100)",
    # 흔들리는 효과 (Angry): 좌우 회전으로 진동
    "쉐이크": r"\t(0,80,\frz4)\t(80,160,\frz-4)\t(160,240,\frz4)\t(240,320,\frz-4)\t(320,400,\frz0)",
    # 페이드인/아웃 (Sad): 부드럽게 나타났다 사라짐
    "페이드": r"\fad(400,400)",
    # 효과 없음
    "없음": "",
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
    effect: Optional[str] = "없음"


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
        margin_v = POSITION_MARGIN_V.get(pos_key, 400)
        font_size = (seg.fontSize or 20) * FONT_SIZE_SCALE
        effect_tag = EFFECT_OVERRIDE.get(seg.effect or "없음", "")

        override = (
            f"{{\\an{alignment}"
            f"\\fn{font_name}"
            f"\\fs{font_size}"
            f"\\c{color_ass}"
            f"{effect_tag}"
            f"}}"
        )
        text = seg.text.replace("\n", "\\N").replace("\r", "")

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
