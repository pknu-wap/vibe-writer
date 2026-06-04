import "./intro.css";
import TopNav from "./components/top-nav";
import Link from "next/link";

export default function Home() {
  return (
    <div className="intro-container">


      <TopNav />

    
      <img
        src="/vibe-writer/images/intro-image.png"
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

      <Link href="/upload" className="start-button">
        지금 시작하기
      </Link>

    </div>
  );
}
