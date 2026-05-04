import streamlit as st
from loading import show_loading

st.set_page_config(page_title="VIBE-WRITER", layout="centered")

if st.session_state.get("page") != "loading":
    st.session_state["page"] = "upload"
#css
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(112.74deg, #190022 5.73%, #000000 89.42%);
}
.block-container {
    max-width: 1000px;
    padding-top: 40px;
}
.nav {
    display: flex;
    align-items: center;
    gap: 20px;
    color: white;
}

.nav-logo {
    font-size: 32px;
    font-weight: 700;
}
.nav-sub {
    font-size: 16px;
    opacity: 0.8;
}

.main-title {
    text-align: center;
    font-size: 72px;
    font-weight: 800;
    color: white;
    margin: 60px 0;
}

.card {
    background: linear-gradient(180deg, #190022 0%, #3B3B3B 100%);
    border: 6px solid white;
    border-radius: 40px;
    padding: 80px 80px;
    text-align: center;
    width: 100%;
    max-width: 700px;
    margin: 0 auto;
}
.circle {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    border: 6px solid white;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 40px;
}

.title {
    font-size: 28px;
    font-weight: 700;
    color: white;
}
.sub {
    font-size: 16px;
    color: white;
    opacity: 0.8;
    margin-bottom: 30px;
}
[data-testid="stFileUploader"] button {
    background: #38293E !important;
    border: 3px solid white !important;
    border-radius: 20px !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    color: white !important;
    padding: 16px !important;
}
[data-testid="stFileUploaderDropzone"] {
    background: transparent !important;
    border: none !important;
}
.upload-wrap {
    margin-top: -140px; 
    display: flex;
    justify-content: center;
}

[data-testid="stFileUploader"] {
    width: 60%;
}
</style>
""", unsafe_allow_html=True)

def film_holes(n=10):
    return ''.join(['<div class="film-hole"></div>'] * n)
if st.session_state["page"] == "upload":
    st.markdown("""
    <div class="nav">
        <div class="nav-logo">VIBE - WRITER</div>
        <div class="nav-sub">AI 감정 기반 숏폼 자막 자동 생성 서비스</div>
    </div>

    <div class="main-title">VIBE - WRITER</div>

    <div class="card">
        <div class="circle">
            <svg width="60" height="60" viewBox="0 0 100 100" fill="none"
                xmlns="http://www.w3.org/2000/svg">
                <path d="M50 75L18.75 43.75L27.5 34.6875L43.75 50.9375V0H56.25V50.9375L72.5 34.6875L81.25 43.75L50 75ZM12.5 100C9.0625 100 6.12083 98.7771 3.675 96.3313C1.22917 93.8854 0.00416667 90.9417 0 87.5V68.75H12.5V87.5H87.5V68.75H100V87.5C100 90.9375 98.7771 93.8812 96.3313 96.3313C93.8854 98.7812 90.9417 100.004 87.5 100H12.5Z"
                    fill="white"/>
            </svg>
        </div>
        <div class="title">영상을 여기에 첨부 해 주세요.</div>
        <div class="sub">새로형(9:16), 60초 이내, MP4</div>

    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 4, 1])
    with col_c:
        st.markdown('<div class="upload-wrap">', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "영상 선택하기",
            type=["mp4"],
            label_visibility="collapsed"
        )

        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded_file:
            st.session_state["file"] = uploaded_file
            st.session_state["page"] = "loading"
            st.rerun()

elif st.session_state["page"] == "loading":
    show_loading()