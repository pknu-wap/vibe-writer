from moviepy import VideoFileClip
import os

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


if __name__ == "__main__":
    result = extract_audio("")
    print(result)

    frame = get_still_cut("", 3.0)
    print(frame.shape)

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
    """폰트 로드. 실패 시 기본 폰트 반환."""
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
    """
    영상 프레임에 감정 기반 자막을 렌더링합니다.
 
    Parameters
    ----------
    frame         : H×W×3 BGR numpy array (OpenCV 포맷)
    text          : 표시할 자막 문자열
    emotion       : 'Happy' | 'Angry' | 'Sad' | 'Neutral'
    font_variant  : 감정별 폰트 키 (없으면 default_font 사용)
                    Happy   → 'mallang' | 'griun'
                    Sad     → 'kcc' | 'daechung'
                    Angry   → 'ongleaf' | 'mulmaru'
                    Neutral → 'pretendard'
    style_preset  : {'color': '#RRGGBB', 'font_size': int, 'font_path': str} 형태로
                    직접 넘기면 emotion 프리셋 전체를 무시하고 사용
 
    Returns
    -------
    frame_out : 자막이 합성된 H×W×3 BGR numpy array
 
    Examples
    --------
    >>> render_subtitle(frame, "신난다!", emotion="Happy")
    >>> render_subtitle(frame, "신난다!", emotion="Happy", font_variant="griun")
    >>> render_subtitle(frame, "슬퍼", emotion="Sad", font_variant="daechung")
    >>> render_subtitle(frame, "분노", emotion="Angry", font_variant="mulmaru")
    """
 
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
    """
    영상 전체 프레임에 자막을 렌더링하여 frames/ 폴더에 저장합니다.
 
    Parameters
    ----------
    video_path   : 원본 영상 파일 경로
    segments     : AI 반환값 리스트. 각 항목은 아래 형태:
                   {'text': str, 'start': float, 'end': float, 'emotion': str}
                   start/end 단위는 초(seconds)
    output_dir   : 프레임 저장 폴더 (기본값: 'frames')
    font_variant : render_subtitle에 넘길 폰트 키 (없으면 emotion별 default 사용)
 
    Returns
    -------
    output_dir : 저장된 프레임 폴더 경로 (merge_video에 바로 넘길 수 있음)
 
    Examples
    --------
    >>> segments = [
    ...     {'text': '안녕하세요', 'start': 0.0,  'end': 3.5,  'emotion': 'Happy'},
    ...     {'text': '슬프다',    'start': 3.5,  'end': 7.0,  'emotion': 'Sad'},
    ... ]
    >>> frame_dir = render_all_frames('input.mp4', segments)
    >>> merge_video(frame_dir, ...)
    """
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