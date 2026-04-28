import streamlit as st
from loading import show_loading

st.set_page_config(page_title="VIBE-WRITER", layout="centered")

if "page" not in st.session_state:
    st.session_state["page"] = "upload"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Noto+Sans+KR:wght@400;600;700&display=swap');

[data-testid="stAppViewContainer"] { background: #fff; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem !important; max-width: 800px !important; }

.nav {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-bottom: 17px;
    border-bottom: none;
    background: linear-gradient(to bottom, #ddd, #fff) no-repeat bottom / 100% 1.5px;
    margin-bottom: 48px;
}
.nav-logo {
    font-family: 'Barlow Condensed Black', sans-serif;
    font-weight: 900;
    font-size: 25px;
    letter-spacing: 2px;
    color: #828598;
}
.nav-sub { font-size: 12px; font-weight: 700; color: #828598; font-family: 'Noto Sans KR', sans-serif; }

.main-title {
    font-family: 'Barlow Condensed Black', sans-serif;
    font-size: 80px;
    font-weight: 900;
    color: #828598;
    text-align: center;
    line-height: 1;
    margin-bottom: 40px;
}

.card {
    position: relative;
    background: linear-gradient(170deg, #d8dcff 0%, #c8d0f0 50%, #9395ac 100%);
    border-radius: 28px;
    padding: 52px 80px 44px;
    text-align: center;
    overflow: hidden;
}
.film {
    position: absolute;
    top: 0; bottom: 0;
    width: 40px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    padding: 18px 0;
}
.film.left { left: 0; }
.film.right { right: 0; }
.film-hole {
    width: 20px; height: 20px;
    background: rgba(255,255,255,0.9);
}
.icon-wrap {
    width: 130px; height: 130px;
    border-radius: 50%;
    background: rgba(255,255,255);
    display: flex; align-items: center; justify-content: center;
    margin: 0 auto 24px;
}
.card-title {
    font-family: 'Noto Sans KR', sans-serif;
    font-size: 20px; font-weight: 900;
    color: #fff;
}
.card-hint {
    font-size: 13px;
    color: rgba(255,255,255);
    font-family: 'Noto Sans KR', sans-serif;
    margin-bottom: 0;
}

[data-testid="stFileUploaderDropzone"] {
    background: #fff !important;
    border: none !important;
    border-radius: 16px !important;
    padding: 4px !important;
}
[data-testid="stFileUploader"] button {
    background: #fff !important;
    color: #4a4870 !important;
    border: none !important;
    border-radius: 16px !important;
    font-family: 'Noto Sans KR', sans-serif !important;
    font-weight: 700 !important;
    font-size: 18px !important;
    padding: 16px 0 !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

def film_holes(n=10):
    return ''.join(['<div class="film-hole"></div>'] * n)

if st.session_state["page"] == "upload":
    st.markdown(f"""
    <div class="nav">
        <span class="nav-logo">VIBE - WRITER</span>
        <span class="nav-sub">AI 감정 기반 숏폼 자막 자동 생성 서비스</span>
    </div>
    <div class="main-title">VIBE - WRITER</div>
    <div class="card">
        <div class="film left">{film_holes()}</div>
        <div class="film right">{film_holes()}</div>
        <div class="icon-wrap">
            <svg width="80" height="80" viewBox="0 0 80 80" fill="none"
                stroke="#6e6c90" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="40" y1="24" x2="40" y2="52"/>
            <polyline points="28,42 40,54 52,42"/>
            </svg>
        </div>
        <div class="card-title">영상을 여기에 첨부 해 주세요.</div>
        <div class="card-hint">새로형(9:16), 60초 이내, MP4</div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 4, 1])
    with col_c:
        uploaded_file = st.file_uploader("영상 선택하기", type=["mp4"], label_visibility="collapsed")
        if uploaded_file:
            st.session_state["file"] = uploaded_file
            st.session_state["page"] = "loading"
            st.rerun()

elif st.session_state["page"] == "loading":
    show_loading()
