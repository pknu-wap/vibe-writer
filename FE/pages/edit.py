import streamlit as st
import streamlit.components.v1 as components


st.markdown("""
<style>
html, body, .stApp {
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}

.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}

header, footer,
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
}

iframe {
    width: 100vw !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)


html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html, body {
    width: 100%;
    height: 100%;
    background: #222;
    font-family: Arial, sans-serif;
    overflow: hidden;
}

.app {
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-direction: column;
    background: #222;
}

/* 상단 제목 */
.header {
    height: 105px;
    background: white;
    color: black;
    border-top: 8px solid #222;
    border-bottom: 1px solid black;
    display: flex;
    align-items: center;
    gap: 22px;
    padding: 0 30px;
}

.header h1 {
    font-size: 44px;
    font-weight: 900;
    letter-spacing: 1px;
}

.header p {
    font-size: 19px;
}

/* 본문 3분할 */
.main {
    flex: 1;
    display: grid;
    grid-template-columns: 400px 1fr 360px;
    min-height: 0;
}

/* 왼쪽, 오른쪽 패널 */
.side {
    background: black;
    color: white;
}

.side-title {
    height: 55px;
    background: white;
    color: black;
    border-bottom: 1px solid black;
    padding: 16px 25px;
    font-weight: bold;
    display: flex;
    justify-content: space-between;
    align-items: center;
}


.side-body {
    padding: 30px 24px;
}

.label {
    font-size: 13px;
    margin-top: 20px;
    margin-bottom: 10px;
}

input[type="range"] {
    width: 100%;
}

/* 버튼 */
.btns {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

#effectBtns {
    flex-wrap: nowrap;
}

button {
    min-width: 75px;
    border: none;
    border-radius: 20px;
    background: white;
    color: black;
    padding: 6px 14px;
    font-size: 14px;
    cursor: pointer;
}

button.on {
    background: gray;
}

/* 가운데 미리보기 */
.center {
    background: white;
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.preview {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}

.phone {
    width: 235px;
    height: 385px;
    background: #d8d8d8;
    position: relative;
}

.circle {
    width: 64px;
    height: 64px;
    background: #222;
    border-radius: 50%;
    position: absolute;
    left: 50%;
    top: 47%;
    transform: translate(-50%, -50%);
    display: flex;
    justify-content: center;
    align-items: center;
}

.circle span {
    width: 48px;
    height: 48px;
    background: #7f89a8;
    color: white;
    border-radius: 50%;
    text-align: center;
    line-height: 48px;
    font-size: 30px;
}

.subtitle {
    position: absolute;
    top: 20px;
    left: 0;
    right: 0;
    color: white;
    font-size: 28px;
    font-weight: bold;
    text-align: center;
    text-shadow: 1px 1px 4px black;
}

/* 자막 효과 */
@keyframes bounce {
    0% { margin-top: 0; }
    50% { margin-top: -8px; }
    100% { margin-top: 0; }
}

@keyframes fade {
    0% { opacity: 0.2; }
    100% { opacity: 1; }
}

@keyframes shake {
    0% { margin-left: 0; }
    25% { margin-left: -6px; }
    50% { margin-left: 6px; }
    75% { margin-left: -6px; }
    100% { margin-left: 0; }
}

.bounce {
    animation: bounce 0.7s infinite;
}

.fade {
    animation: fade 0.8s infinite alternate;
}

.shake {
    animation: shake 0.4s infinite;
}

/* 하단 재생바 */
.player {
    height: 55px;
    background: #d9d9d9;
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 0 20px;
}

.play {
    width: 30px;
    height: 30px;
    background: black;
    border-radius: 50%;
    position: relative;
}

.play::after {
    content: "";
    position: absolute;
    left: 12px;
    top: 8px;
    border-left: 10px solid white;
    border-top: 7px solid transparent;
    border-bottom: 7px solid transparent;
}

.line {
    flex: 1;
    height: 10px;
    background: white;
    border-radius: 20px;
}

.time {
    color: black;
    font-size: 12px;
}

/* 감정 버튼 */
.emotion {
    height: 74px;
    border: 4px solid white;
    border-radius: 8px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 22px;
    padding-left: 28px;
    cursor: pointer;
}

.emotion.on {
    border-color: gray;
}

.dot {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    flex-shrink: 0;
}

.emotion-name {
    font-size: 28px;
    color: white;
    margin-right: 10px;
}

.emotion-desc {
    font-size: 12px;
    color: gray;
}
</style>
</head>

<body>
<div class="app">

    <div class="header">
        <h1>VIBE - WRITER</h1>
        <p>AI 감정 기반 숏폼 자막 자동 생성 서비스</p>
    </div>

    <div class="main">

        <div class="side">
            <div class="side-title">
                <span>스타일 설정</span>
                
            </div>

            <div class="side-body">

                <div class="label">글자 크기</div>
                <input type="range" id="size" min="12" max="70" value="28">

                <div class="label">위치</div>
                <div class="btns" id="positionBtns">
                    <button onclick="setPosition('bottom', this)">하단</button>
                    <button onclick="setPosition('middle', this)">중앙</button>
                    <button class="on" onclick="setPosition('top', this)">상단</button>
                </div>

                <div class="label">효과</div>
                <div class="btns" id="effectBtns">
                    <button class="on" onclick="setEffect('bounce', this)">바운스</button>
                    <button onclick="setEffect('fade', this)">페이드</button>
                    <button onclick="setEffect('shake', this)">쉐이크</button>
                    <button onclick="setEffect('none', this)">없음</button>
                </div>

                <div class="label">폰트</div>
                <div class="btns" id="fontBtns">
                    <button class="on" onclick="setFont('bold', this)">통통체</button>
                    <button onclick="setFont('900', this)">각진체</button>
                    <button onclick="setFont('normal', this)">얇은체</button>
                    <button onclick="setFont('500', this)">고딕</button>
                </div>

            </div>
        </div>

        <div class="center">
            <div class="preview">
                <div class="phone">
                    <div class="circle">
                        <span>S</span>
                    </div>
                    <div class="subtitle bounce" id="subtitle">미리보기</div>
                </div>
            </div>

            <div class="player">
                <div class="play"></div>
                <div class="line"></div>
                <div class="time">0:12 / 0:35</div>
            </div>
        </div>

        <div class="side">
            <div class="side-title">
                <span>감정 설정</span>
                
            </div>

            <div class="side-body">

                <div class="emotion on" onclick="setEmotion('#ffdb3d', 65, 'bold', this)">
                    <div class="dot" style="background:#ffdb3d"></div>
                    <div>
                        <span class="emotion-name">Happy</span>
                        <span class="emotion-desc">통통체 - 65px</span>
                    </div>
                </div>

                <div class="emotion" onclick="setEmotion('#ef3324', 70, '900', this)">
                    <div class="dot" style="background:#ef3324"></div>
                    <div>
                        <span class="emotion-name">Angry</span>
                        <span class="emotion-desc">각진체 - 70px</span>
                    </div>
                </div>

                <div class="emotion" onclick="setEmotion('#5fc0f0', 45, 'normal', this)">
                    <div class="dot" style="background:#5fc0f0"></div>
                    <div>
                        <span class="emotion-name">Sad</span>
                        <span class="emotion-desc">얇은체 - 45px</span>
                    </div>
                </div>

                <div class="emotion" onclick="setEmotion('#aaaaaa', 50, '500', this)">
                    <div class="dot" style="background:#e8e8e8"></div>
                    <div>
                        <span class="emotion-name">Neutral</span>
                        <span class="emotion-desc">고딕 - 50px</span>
                    </div>
                </div>

            </div>
        </div>

    </div>
</div>

<script>
let subtitle = document.getElementById("subtitle");
let size = document.getElementById("size");

size.oninput = function() {
    subtitle.style.fontSize = size.value + "px";
}

function buttonOn(areaId, button) {
    let buttons = document.querySelectorAll("#" + areaId + " button");

    for (let i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("on");
    }

    button.classList.add("on");
}

function setPosition(position, button) {
    buttonOn("positionBtns", button);

    if (position == "top") {
        subtitle.style.top = "20px";
        subtitle.style.bottom = "auto";
        subtitle.style.transform = "none";
    }

    if (position == "middle") {
        subtitle.style.top = "50%";
        subtitle.style.bottom = "auto";
        subtitle.style.transform = "translateY(-50%)";
    }

    if (position == "bottom") {
        subtitle.style.top = "auto";
        subtitle.style.bottom = "20px";
        subtitle.style.transform = "none";
    }
}

function setEffect(effect, button) {
    buttonOn("effectBtns", button);

    subtitle.classList.remove("bounce");
    subtitle.classList.remove("fade");
    subtitle.classList.remove("shake");

    if (effect != "none") {
        subtitle.classList.add(effect);
    }
}

function setFont(weight, button) {
    buttonOn("fontBtns", button);
    subtitle.style.fontWeight = weight;
}

function setEmotion(color, fontSize, weight, box) {
    let boxes = document.querySelectorAll(".emotion");

    for (let i = 0; i < boxes.length; i++) {
        boxes[i].classList.remove("on");
    }

    box.classList.add("on");

    subtitle.style.color = color;
    subtitle.style.fontSize = fontSize + "px";
    subtitle.style.fontWeight = weight;
    size.value = fontSize;
}
</script>

</body>
</html>
"""

components.html(html_code, height=820, scrolling=False)