import Link from "next/link";
import Image from "next/image";
import heroImage from "../../public/vibe-hero.png";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#190022] to-black relative overflow-hidden">
      <div className="absolute left-[3%] top-[3%] flex items-baseline gap-4">
        <h1 className="text-3xl font-black tracking-wide text-white">
          VIBE - WRITER
        </h1>
        <p className="text-sm text-white/80">
          AI 감정 기반 숏폼 자막 자동 생성 서비스
        </p>
      </div>

      <Image
        src={heroImage}
        alt=""
        className="absolute right-[5%] top-[20%] w-[45vw] max-w-[700px] h-auto object-contain"
        priority
      />

      <p className="absolute left-[7%] top-[40%] text-2xl text-white leading-relaxed">
        감정을 읽고,
        <br />
        자막을 자동으로 만들어줍니다.
      </p>

      <h2 className="absolute left-[7%] top-[55%] text-[8vw] font-black text-white leading-none tracking-tight">
        VIBE - WRITER
      </h2>

      <Link
        href="/upload"
        className="absolute right-[5%] bottom-[8%] text-2xl font-black text-white hover:opacity-80 transition-opacity"
      >
        지금 시작하기
      </Link>
    </div>
  );
}
