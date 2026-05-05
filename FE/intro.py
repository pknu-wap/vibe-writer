import streamlit as st
import base64

def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = img_to_base64("image.png")

st.set_page_config(page_title="VIBE - WRITER", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&family=Noto+Sans+KR&display=swap');

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.vibe-card {
    width: 100vw;
    height: 98vh;
    background: linear-gradient(112.74deg, #190022 5.73%, #000000 89.42%);
    position: relative;
    overflow: hidden;
    font-family: 'Inter', 'Noto Sans KR', sans-serif;
}

.vibe-image {
    position: absolute;
    width: 40vw;
    height: 30vw;
    right: 5%;
    top: 20%;
}

.vibe-image img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
            
.vibe-logo {
    position: absolute;
    left: 3%;
    top: 3%;
    font-size: 2.5vw;
    font-weight: 700;
    color: white;
}

.vibe-subtitle {
    position: absolute;
    left: 25%;
    top: 5%;
    font-size: 1.2vw;
    color: white;
}

.vibe-desc {
    position: absolute;
    left: 7%;
    top: 40%;
    font-size: 2.5vw;
    color: white;
    line-height: 1.3;
}

.vibe-title-big {
    position: absolute;
    left: 7%;
    top: 55%;
    font-size: 6vw;
    font-weight: 900;
    color: white;
}

div.stButton {
    position: fixed;
    left: 50%;
    bottom: 8%;
    transform: translateX(-50%);
    z-index: 999;
}
            
div.stButton > button {
    all: unset;
    cursor: pointer;

    font-size: clamp(14px, 1.2vw, 20px);
    font-weight: 900;
    padding: 14px 40px;
    border-radius: 50px;

    background: linear-gradient(135deg, #190022, #3B3B3B);
    color: white;

    box-shadow: 0 10px 30px rgba(0,0,0,0.6);
    transition: all 0.25s ease;
}

div.stButton > button:hover {
    transform: translateY(-3px) scale(1.05);
}
</style>
""", unsafe_allow_html=True)




st.markdown(f"""
<div class="vibe-card">
    <div class="vibe-image">
        <img src="data:image/png;base64,{img}">
    </div>
    <div class="vibe-logo">VIBE - WRITER</div>
    <div class="vibe-subtitle">AI 감정 기반 숏폼 자막 자동 생성 서비스</div>
    <div class="vibe-desc">
        감정을 읽고,<br>
        자막을 자동으로 만들어줍니다.
    </div>
    <div class="vibe-title-big">VIBE - WRITER</div>
</div>
""", unsafe_allow_html=True)


if st.button("지금 시작하기>>>"):
    st.switch_page("pages/upload.py")