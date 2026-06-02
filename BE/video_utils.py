from moviepy import VideoFileClip
import os
import logging

logger = logging.getLogger(__name__)

def extract_audio(video_path):
    video = VideoFileClip(video_path)
    audio = video.audio
    
    base = os.path.splitext(video_path)[0]
    audio_path = base + ".wav"
    
    audio.write_audiofile(audio_path)
    video.close()
    
    return audio_path

def get_still_cut(video_path, timestamp):
    video = VideoFileClip(video_path)
    frame = video.get_frame(timestamp)
    video.close()
    
    return frame


import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np


EMOTION_STYLE: dict[str, dict] = {
    "Happy": {
        "color": "#FFB300",
        "font_size": 65,
        "fonts": {
            "mallang": "assets/fonts/Ok Mallang B.ttf",
            "griun":   "assets/fonts/Griun_Mongtori-Rg.ttf",
        },
        "default_font": "mallang",
    },
    "Sad": {
        "color": "#42A5F5",
        "font_size": 45,
        "fonts": {
            "kcc":      "assets/fonts/KCC-Kimhwanki.ttf",
            "daechung": "assets/fonts/RF대충쓴준우체v3.ttf",
        },
        "default_font": "kcc",
    },
    "Angry": {
        "color": "#E53935",
        "font_size": 70,
        "fonts": {
            "ongleaf": "assets/fonts/온글잎_바닷바람.ttf",
            "mulmaru": "assets/fonts/Mulmaru.ttf",
        },
        "default_font": "ongleaf",
    },
    "Neutral": {
        "color": "#FFFFFF",
        "font_size": 50,
        "fonts": {
            "pretendard": "assets/fonts/Pretendard-Regular.ttf",
        },
        "default_font": "pretendard",
    },
}
 
DEFAULT_STYLE = EMOTION_STYLE["Neutral"]
 
def _hex_to_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (r, g, b, alpha)
 
 
def _load_font(font_path: str, font_size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(font_path, font_size)
    except Exception:
        return ImageFont.load_default(size=font_size)

def render_subtitle(
    frame: np.ndarray,
    text: str,
    emotion: str = "Neutral",
    font_variant: str | None = None,
    style_preset: dict | None = None,
) -> np.ndarray:
    if style_preset:
        color     = style_preset.get("color", "#FFFFFF")
        font_size = style_preset.get("font_size", 50)
        font_path = style_preset.get("font_path", "")
        font      = _load_font(font_path, font_size)
    else:
        style     = EMOTION_STYLE.get(emotion, DEFAULT_STYLE)
        color     = style["color"]
        font_size = style["font_size"]
        variant   = font_variant or style["default_font"]
        font_path = style["fonts"].get(variant, list(style["fonts"].values())[0])
        font      = _load_font(font_path, font_size)
 
    text_color_rgba = _hex_to_rgba(color)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img   = Image.fromarray(frame_rgb).convert("RGBA")
    overlay   = Image.new("RGBA", pil_img.size, (0, 0, 0, 0))
    draw      = ImageDraw.Draw(overlay)
 
    img_w, img_h = pil_img.size
    bbox   = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (img_w - text_w) // 2
    y = int(img_h * 0.92) - text_h

    shadow_offset = max(2, font_size // 20)
    draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 180))
    draw.text((x, y), text, font=font, fill=text_color_rgba)
 
    combined  = Image.alpha_composite(pil_img, overlay).convert("RGB")
    frame_out = cv2.cvtColor(np.array(combined), cv2.COLOR_RGB2BGR)
    return frame_out


def render_all_frames(
    video_path: str,
    segments: list[dict],
    output_dir: str = "frames",
    font_variant: str | None = None,
) -> str:
    import os
 
    os.makedirs(output_dir, exist_ok=True)
 
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"영상 파일을 열 수 없습니다: {video_path}")
 
    fps        = cap.get(cv2.CAP_PROP_FPS)
    frame_idx  = 0
 
    seg_frames = [
        {
            "start_f": int(s["start"] * fps),
            "end_f":   int(s["end"]   * fps),
            "text":    s["text"],
            "emotion": s.get("emotion", "Neutral"),
        }
        for s in segments
    ]
 
    while True:
        ret, frame = cap.read()
        if not ret:
            break
 
        active = next(
            (s for s in seg_frames if s["start_f"] <= frame_idx < s["end_f"]),
            None,
        )
 
        if active:
            frame = render_subtitle(
                frame,
                text=active["text"],
                emotion=active["emotion"],
                font_variant=font_variant,
            )
 
        filename = os.path.join(output_dir, f"frame_{frame_idx:06d}.jpg")
        cv2.imwrite(filename, frame)
        frame_idx += 1
 
    cap.release()
    return output_dir
