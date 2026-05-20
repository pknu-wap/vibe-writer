import "./intro.css";

export default function Home() {
  return (
    <div className="intro-container">
      
      <div className="top-bar">
        <h1 className="logo">VIBE - WRITER</h1>

        <div className="line"></div>

        <p className="service-text">
          AI 감정 기반 숏폼 자막 자동 생성 서비스
        </p>
      </div>

    
      <img
        src="/images/intro-image.png"
        alt="main"
        className="main-image"
      />

      <div className="main-text">
        감정을 읽고,
        <br />
        자막을 자동으로 만들어줍니다.
      </div>

      
      <h1 className="main-title">
        VIBE - WRITER
      </h1>

      
      <button className="start-button">
        지금 시작하기
      </button>
    </div>
  );
}