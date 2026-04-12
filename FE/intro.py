import streamlit as st
from upload import show_upload
from loading import show_loading

st.set_page_config(page_title="VIBE-WRITER", layout="wide")

if "page" not in st.session_state:
    st.session_state["page"] = "intro"

def show_intro():
    st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap');

  [data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #8F6B9E 0%, #332638 100%) !important;
  }
  [data-testid="stAppViewBlockContainer"] {
    padding: 0 !important;
  }

  .main-wrapper {
    position: relative;
    width: 100%;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
    overflow: hidden;
  }

  .navbar {
    width: 100%;
    height: 110px;
    background: rgba(255, 255, 255, 0.1);
    box-shadow: 0px 4px 30px rgba(0, 0, 0, 0.25);
    display: flex;
    align-items: center;
    padding: 0 15px;
    box-sizing: border-box;
  }
  .navbar-logo {
    font-weight: 900;
    font-size: clamp(28px, 4vw, 48px);
    color: #FFFFFF;
    white-space: nowrap;
  }
  .navbar-sub {
    font-weight: 400;
    font-size: clamp(13px, 1.5vw, 20px);
    color: #FFFFFF;
    margin-left: clamp(20px, 3vw, 60px);
    white-space: nowrap;
  }

  .emoji-layer {
    position: absolute;
    top: 110px;
    left: 0;
    width: 100%;
    height: calc(100% - 110px);
    pointer-events: none;
    z-index: 1;
  }
  .em1 { position: absolute; left: 61.9%; top: 15px;  font-size: clamp(80px, 12vw, 170px); opacity: 0.44; filter: blur(5px);   transform: rotate(-12.94deg); line-height: 1; }
  .em2 { position: absolute; left: 74.6%; top: 63px;  font-size: clamp(100px,14vw, 200px); opacity: 0.6;  filter: blur(2.5px); transform: rotate(6.59deg);   line-height: 1; }
  .em3 { position: absolute; left: 49.2%; top: 139px; font-size: clamp(110px,16vw, 220px); opacity: 0.8;  filter: blur(1.5px);                               line-height: 1; }
  .em4 { position: absolute; left: 61.5%; top: 190px; font-size: clamp(120px,18vw, 250px); opacity: 0.9;  filter: blur(0.5px); transform: rotate(15.69deg);  line-height: 1; }

  .hero {
    position: relative;
    z-index: 2;
    padding: clamp(60px, 8vw, 170px) clamp(30px, 6.7vw, 97px) 0;
  }
  .hero-sub {
    font-weight: 400;
    font-size: clamp(20px, 3.3vw, 48px);
    line-height: 1.4;
    color: #FFFFFF;
    margin: 0 0 16px 0;
  }
  .hero-title {
    font-weight: 900;
    font-size: clamp(48px, 9vw, 128px);
    line-height: 1.21;
    background: linear-gradient(180deg, #FFFFFF 50%, #999999 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0px 4px 20px rgba(0,0,0,0.25));
    margin: 0;
    word-break: keep-all;
  }

  .stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 900 !important;
    font-size: 24px !important;
    color: #FFFFFF !important;
    background: rgba(255, 255, 255, 0.15) !important;
    border: 2px solid rgba(255, 255, 255, 0.6) !important;
    border-radius: 12px !important;
    padding: 14px 32px !important;
    height: auto !important;
    transition: all 0.2s !important;
  }
  .stButton > button:hover {
    background: rgba(255, 255, 255, 0.28) !important;
    border-color: #FFFFFF !important;
    color: #FFFFFF !important;
  }
</style>

<div class="main-wrapper">
  <nav class="navbar">
    <span class="navbar-logo">VIBE - WRITER</span>
    <span class="navbar-sub">AI 감정 기반 숏폼 자막 자동 생성 서비스</span>
  </nav>

  <div class="emoji-layer">
    <span class="em1">😭</span>
    <span class="em2">😡</span>
    <span class="em3">😂</span>
    <span class="em4">😊</span>
  </div>

  <div class="hero">
    <p class="hero-sub">감정을 읽고,<br>자막을 자동으로 만들어줍니다.</p>
    <h1 class="hero-title">VIBE - WRITER</h1>
  </div>
</div>
""", unsafe_allow_html=True)

    _, _, col_btn = st.columns([3, 3, 2])
    with col_btn:
        if st.button("지금 시작하기 >>"):
            st.session_state["page"] = "upload"
            st.rerun()

if st.session_state["page"] == "intro":
    show_intro()
elif st.session_state["page"] == "upload":
    show_upload()
elif st.session_state["page"] == "loading":
    show_loading()