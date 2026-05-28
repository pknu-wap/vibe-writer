import Link from "next/link";
import "./top-nav.css";

export default function TopNav() {
  return (
    <div className="top-bar">
      <Link href="/" className="logo-link">
        <h1 className="logo">VIBE - WRITER</h1>
      </Link>

      <div className="line"></div>

      <p className="service-text">
        AI 감정 기반 숏폼 자막 자동 생성 서비스
      </p>
    </div>
  );
}