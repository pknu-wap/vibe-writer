import streamlit as st

st.set_page_config(page_title="VIBE-WRITER", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;900&display=swap" rel="stylesheet">
<style>
@import url('https://fonts.cdnfonts.com/css/nippo');
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
background: linear-gradient(112.74deg, #190022 5.73%, #000000 89.42%) !important;
}
[data-testid="stHeader"], [data-testid="stToolbar"], #MainMenu, footer { display: none !important; }
[data-testid="stAppViewContainer"] > .main > .block-container {
padding: 2.5rem 3.5rem !important;
max-width: 100% !important;
}
.vw-logo { font-family: 'Nippo', sans-serif; font-weight: 700; font-size: 48px; color: #fff; display: inline; }
.vw-tagline { font-family: 'Inter', sans-serif; font-size: 20px; color: #fff; margin-left: 24px; display: inline; }
.vw-complete-row { display: flex; align-items: center; gap: 14px; margin-bottom: 16px; }
.vw-check-circle { width: 52px; height: 52px; background: #00FF37; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.vw-complete-text { font-family: 'Inter', sans-serif; font-weight: 900; font-size: 48px; color: #fff; }
.vw-emotion-row { display: flex; gap: 12px; margin-bottom: 24px; }
.vw-emotion-tag { height: 50px; padding: 0 24px; border-radius: 20px; font-family: 'Nippo', sans-serif; font-weight: 700; font-size: 22px; display: flex; align-items: center; }
.tag-happy   { background: #FFD500; color: #fff; }
.tag-angry   { background: #FF0000; color: #fff; }
.tag-sad     { background: #00C8FF; color: #fff; }
.tag-neutral { background: #D9D9D9; color: #555; }
div[data-testid="stDownloadButton"] button {
width: 100% !important; height: 130px !important;
background: #000 !important; border: 5px solid #fff !important;
border-radius: 20px !important; font-family: 'Inter', sans-serif !important;
font-weight: 900 !important; font-size: 32px !important; color: #fff !important;
}
div[data-testid="stButton"] button {
width: 100% !important; height: 130px !important;
background: #fff !important; border: 5px solid #000 !important;
border-radius: 20px !important; font-family: 'Inter', sans-serif !important;
font-weight: 900 !important; font-size: 32px !important; color: #000 !important;
}
</style>
""", unsafe_allow_html=True)

if "go_edit" not in st.session_state:
    st.session_state.go_edit = False
if st.session_state.go_edit:
    st.session_state.go_edit = False
    st.switch_page("pages/upload.py")

video_bytes = st.session_state.get("result_video", None)


st.markdown("<span class=\"vw-logo\">VIBE - WRITER</span><span class=\"vw-tagline\">AI 감정 기반 숏폼 자막 자동 생성 서비스</span>", unsafe_allow_html=True)

st.write("")
st.write("")

_, right = st.columns([1, 2])

with right:
    st.markdown(
"<div class=\"vw-complete-row\">"
"<div class=\"vw-check-circle\">"
"<svg width=\"24\" height=\"20\" viewBox=\"0 0 24 20\" fill=\"none\">"
"<path d=\"M2 10L9 17L22 3\" stroke=\"white\" stroke-width=\"4\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>"
"</svg>"
"</div>"
"<div class=\"vw-complete-text\">완성됐어요!</div>"
"</div>"
"<div class=\"vw-emotion-row\">"
"<div class=\"vw-emotion-tag tag-happy\">happy</div>"
"<div class=\"vw-emotion-tag tag-angry\">Angry</div>"
"<div class=\"vw-emotion-tag tag-sad\">Sad</div>"
"<div class=\"vw-emotion-tag tag-neutral\">Netural</div>"
"</div>",
    unsafe_allow_html=True)

    if video_bytes:
        st.download_button("다운로드", data=video_bytes, file_name="output.mp4", mime="video/mp4", use_container_width=True)
    else:
        st.download_button("다운로드", data=b"", file_name="output.mp4", mime="video/mp4", use_container_width=True, disabled=True)

    if st.button("다시 편집하기", use_container_width=True):
        st.session_state.go_edit = True
        st.rerun()