import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="VIBE - WRITER", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
  .main .block-container          { padding: 0 !important; max-width: 100% !important; }
  header, footer                  { display: none !important; }
  [data-testid="stSidebar"]        { display: none !important; }
  [data-testid="collapsedControl"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

HTML_APP = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
#폰트 및 색상 수정 필요
  :root {
    --bg:         #0d0d0d;
    --panel:      #141414;
    --panel2:     #1a1a1a;
    --border:     #2a2a2a;
    --border2:    #333;
    --text:       #e8e8e8;
    --text-muted: #777;
    --text-dim:   #555;
    --pill-bg:    #1f1f1f;
    --pill-active:#3a3a3a;
  }

  html, body {
    height: 100%;
    background: var(--bg);
    color: var(--text);
    font-family: 'Noto Sans KR', sans-serif;
    overflow: hidden;
  }

  .app  { display: flex; flex-direction: column; height: 100vh; }
  .main { display: grid; grid-template-columns: 220px 1fr 260px; flex: 1; overflow: hidden; }

  .titlebar {
    display: flex; align-items: center; gap: 14px;
    padding: 0 24px; height: 52px;
    border-bottom: 1px solid var(--border); flex-shrink: 0;
  }
  .titlebar h1  { font-size: 22px; font-weight: 700; letter-spacing: -0.5px; color: #fff; }
  .titlebar .sub { font-size: 12px; color: var(--text-muted); }

  .panel {
    background: var(--panel);
    border-right: 1px solid var(--border);
    display: flex; flex-direction: column; overflow: hidden;
  }
  .panel.right { border-right: none; border-left: 1px solid var(--border); }

  .panel-header {
    padding: 12px 16px;
    border-bottom: 1px solid var(--border); flex-shrink: 0;
  }
  .panel-title { font-size: 13px; font-weight: 500; }

  .panel-body {
    flex: 1; overflow-y: auto; padding: 14px;
    display: flex; flex-direction: column; gap: 14px;
  }
  .panel-body::-webkit-scrollbar { width: 4px; }
  .panel-body::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

  .field       { display: flex; flex-direction: column; gap: 6px; }
  .field-label { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.05em; }

  .slider-row { display: flex; align-items: center; gap: 8px; }
  input[type="range"] {
    flex: 1; -webkit-appearance: none;
    height: 3px; background: var(--border2); border-radius: 2px; outline: none; cursor: pointer;
  }
  input[type="range"]::-webkit-slider-thumb {
    -webkit-appearance: none; width: 14px; height: 14px;
    border-radius: 50%; background: #fff; border: 2px solid var(--border2); cursor: pointer;
  }
  .slider-val { font-size: 11px; color: var(--text-muted); min-width: 28px; text-align: right; }

  .pill-group { display: flex; flex-wrap: nowrap; gap: 3px; }
  .pill {
    padding: 3px 8px; border-radius: 100px; font-size: 11px;
    cursor: pointer; border: 1px solid var(--border2); background: var(--pill-bg);
    color: var(--text-muted); transition: all 0.15s; user-select: none; white-space: nowrap;
  }
  .pill:hover  { border-color: #444; color: var(--text); }
  .pill.active { background: var(--pill-active); border-color: #555; color: var(--text); }

  .preview-area {
    background: #1c1c1c;
    display: flex; align-items: center; justify-content: center;
  }

  .video-wrapper {
    position: relative; width: 220px; height: 390px;
    border-radius: 12px; overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
  }
  .video-bg {
    width: 100%; height: 100%;
    background: linear-gradient(160deg, #c4c4c4 0%, #a8a8a8 100%);
  }

  .subtitle-overlay {
    position: absolute; left: 0; right: 0; padding: 0 10px;
    text-align: center; line-height: 1.3; word-break: keep-all;
    text-shadow: 0 1px 4px rgba(0,0,0,0.4);
    transition: color 0.3s, font-size 0.2s;
  }
  .subtitle-overlay.pos-bottom { bottom: 18px; }
  .subtitle-overlay.pos-center { top: 50%; transform: translateY(-50%); }
  .subtitle-overlay.pos-top    { top: 18px; }

  @keyframes bounce { 0%,100%{transform:translateY(0)}  50%{transform:translateY(-4px)} }
  @keyframes shake  { 0%,100%{transform:translateX(0)}  25%{transform:translateX(-3px)} 75%{transform:translateX(3px)} }
  @keyframes fadein { 0%{opacity:0} 100%{opacity:1} }

  .subtitle-overlay.fx-bounce { animation: bounce 0.6s ease infinite; }
  .subtitle-overlay.fx-shake  { animation: shake  0.4s ease infinite; }
  .subtitle-overlay.fx-fade   { animation: fadein 1s   ease infinite alternate; }
  .subtitle-overlay.fx-none   { animation: none; }

  .emotion-btn {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 14px; border-radius: 10px;
    border: 1px solid var(--border2); background: var(--panel2);
    cursor: pointer; transition: border-color 0.15s, background 0.15s; user-select: none;
  }
  .emotion-btn:hover  { border-color: #444; background: #222; }
  .emotion-btn.active { border-color: #555; background: #252525; }
  .emotion-dot  { width: 18px; height: 18px; border-radius: 50%; flex-shrink: 0; }
  .emotion-name { font-size: 14px; font-weight: 500; display: block; }
  .emotion-desc { font-size: 11px; color: var(--text-dim); margin-top: 2px; display: block; }
</style>
</head>
<body>
<div class="app">

  <div class="titlebar">
    <h1>VIBE - WRITER</h1>
    <span class="sub">AI 감정 기반 숏폼 자막 자동 생성 서비스</span>
  </div>

  <div class="main">

    <div class="panel">
      <div class="panel-header"><span class="panel-title">스타일 설정</span></div>
      <div class="panel-body">

        <div class="field">
          <span class="field-label">글자 크기</span>
          <div class="slider-row">
            <input type="range" id="fontSize" min="12" max="70" value="28">
            <span class="slider-val" id="fontSizeVal">28px</span>
          </div>
        </div>

        <div class="field">
          <span class="field-label">위치</span>
          <div class="pill-group" id="posGroup">
            <div class="pill" data-val="pos-bottom">하단</div>
            <div class="pill" data-val="pos-center">중앙</div>
            <div class="pill active" data-val="pos-top">상단</div>
          </div>
        </div>

        <div class="field">
          <span class="field-label">효과</span>
          <div class="pill-group" id="fxGroup">
            <div class="pill active" data-val="fx-bounce">바운스</div>
            <div class="pill" data-val="fx-fade">페이드</div>
            <div class="pill" data-val="fx-shake">쉐이크</div>
            <div class="pill" data-val="fx-none">없음</div>
          </div>
        </div>

        <div class="field">
          <span class="field-label">폰트</span>
          <div class="pill-group" id="fontGroup">
            <div class="pill active" data-val="tong">통통체</div>
            <div class="pill" data-val="gak">각진체</div>
            <div class="pill" data-val="thin">얇은체</div>
            <div class="pill" data-val="gothic">고딕</div>
          </div>
        </div>

      </div>
    </div>

    <div class="preview-area">
      <div class="video-wrapper">
        <div class="video-bg"></div>
        <div class="subtitle-overlay pos-top fx-bounce" id="subtitleOverlay">미리보기</div>
      </div>
    </div>

    <div class="panel right">
      <div class="panel-header"><span class="panel-title">감정 설정</span></div>
      <div class="panel-body">

        <div class="emotion-btn active" data-emotion="happy">
          <div class="emotion-dot" style="background:#f5c542"></div>
          <div>
            <span class="emotion-name">Happy</span>
            <span class="emotion-desc">노란색 · 65px</span>
          </div>
        </div>

        <div class="emotion-btn" data-emotion="angry">
          <div class="emotion-dot" style="background:#e05050"></div>
          <div>
            <span class="emotion-name">Angry</span>
            <span class="emotion-desc">빨간색 · 70px</span>
          </div>
        </div>

        <div class="emotion-btn" data-emotion="sad">
          <div class="emotion-dot" style="background:#5baef5"></div>
          <div>
            <span class="emotion-name">Sad</span>
            <span class="emotion-desc">파란색 · 45px</span>
          </div>
        </div>

        <div class="emotion-btn" data-emotion="neutral">
          <div class="emotion-dot" style="background:#888"></div>
          <div>
            <span class="emotion-name">Neutral</span>
            <span class="emotion-desc">회색 · 50px</span>
          </div>
        </div>

      </div>
    </div>

  </div>
</div>

<script>
  var overlay    = document.getElementById('subtitleOverlay');
  var sizeSlider = document.getElementById('fontSize');
  var sizeVal    = document.getElementById('fontSizeVal');

  var fontWeightMap = { tong:'700', gak:'900', thin:'300', gothic:'500' };

  overlay.style.fontSize   = '28px';
  overlay.style.color      = '#ffffff';
  overlay.style.fontWeight = '700';

  sizeSlider.addEventListener('input', function() {
    overlay.style.fontSize = sizeSlider.value + 'px';
    sizeVal.textContent    = sizeSlider.value + 'px';
  });

  function initPills(groupId, fn) {
    document.getElementById(groupId).querySelectorAll('.pill').forEach(function(pill) {
      pill.addEventListener('click', function() {
        document.getElementById(groupId).querySelectorAll('.pill').forEach(function(p) {
          p.classList.remove('active');
        });
        pill.classList.add('active');
        fn(pill.dataset.val);
      });
    });
  }

  initPills('posGroup', function(val) {
    overlay.classList.remove('pos-bottom', 'pos-center', 'pos-top');
    overlay.classList.add(val);
  });

  initPills('fxGroup', function(val) {
    overlay.classList.remove('fx-bounce', 'fx-fade', 'fx-shake', 'fx-none');
    overlay.classList.add(val);
  });

  initPills('fontGroup', function(val) {
    overlay.style.fontWeight = fontWeightMap[val];
  });

  var emotionPresets = {
    happy:   { color:'#f5c542', size:'65', font:'tong'   },
    angry:   { color:'#e05050', size:'70', font:'gak'    },
    sad:     { color:'#5baef5', size:'45', font:'thin'   },
    neutral: { color:'#aaaaaa', size:'50', font:'gothic' }
  };

  document.querySelectorAll('.emotion-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.emotion-btn').forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');

      var p = emotionPresets[btn.dataset.emotion];
      overlay.style.color      = p.color;
      overlay.style.fontSize   = p.size + 'px';
      overlay.style.fontWeight = fontWeightMap[p.font];

      sizeSlider.value    = p.size;
      sizeVal.textContent = p.size + 'px';

      document.querySelectorAll('#fontGroup .pill').forEach(function(pill) {
        pill.classList.toggle('active', pill.dataset.val === p.font);
      });
    });
  });
</script>
</body>
</html>"""

components.html(HTML_APP, height=700, scrolling=False)