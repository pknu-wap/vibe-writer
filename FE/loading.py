import streamlit as st
import time
from PIL import Image

blank_icon = Image.new("RGBA", (32, 32), (255, 255, 255, 0))

st.set_page_config(
    page_title=" ",
    page_icon=blank_icon,
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;700&display=swap');

.stApp { 
    font-family: 'Noto Sans KR', sans-serif; 
}

.screen-wrap {
    margin-top: 90px;
}

.loader {
    width: 56px;
    height: 56px;
    border: 7px solid #e0e0e0;
    border-top: 7px solid #111;
    border-radius: 50%;
    animation: spin 1.1s linear infinite;
}

@keyframes spin { 
    to { transform: rotate(360deg); } 
}

.film-card {
    background: white;
    border: 3px solid #111;
    border-radius: 18px;
    padding: 60px 44px;
    box-shadow: 6px 6px 0px #111;
    position: relative;
    overflow: hidden;
    width: 380px;
    min-height: 300px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 20px;
    box-sizing: border-box;
}

.holes {
    position: absolute;
    top: 0; 
    bottom: 0;
    width: 24px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    padding: 16px 0;
}

.holes.left  { left: 0; }
.holes.right { right: 0; }

.hole { 
    width: 12px; 
    height: 12px; 
    background: #111; 
    border-radius: 2px; 
}

.status-text {
    font-size: 1.15rem;
    font-weight: 700;
    color: #111;
    text-align: center;
    line-height: 1.5;
    word-break: keep-all;
}

.progress-wrap {
    width: 100%;
    background: #e0e0e0;
    border-radius: 99px;
    height: 12px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: #111;
    border-radius: 99px;
    transition: width 0.3s ease;
}

.progress-text {
    font-size: 0.85rem;
    color: #666;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

HOLES = '<div class="hole"></div>' * 9
FILM_SIDES = f'<div class="holes left">{HOLES}</div><div class="holes right">{HOLES}</div>'

STEPS = [
    ("📂 파일 로드 중",   0.5),
    ("🎙 오디오 추출 중", 0.8),
    ("📝 STT 변환 중",    1.2),
    ("🧠 감정 분석 중",   1.0),
    ("✍️ 자막 생성 중",   0.8),
]

card = st.empty()

for i, (label, delay) in enumerate(STEPS):
    pct = (i + 1) / len(STEPS)
    pct_int = int(pct * 100)

    card.markdown(f"""
    <div class="screen-wrap">
        <div class="film-card">
            {FILM_SIDES}
            <div class="loader"></div>
            <div class="status-text">AI가 감정을 분석하고 자막을 생성하는 중이에요</div>
            <div class="progress-wrap">
                <div class="progress-fill" style="width:{pct_int}%"></div>
            </div>
            <div class="progress-text">{label} ... {pct_int}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    time.sleep(delay)