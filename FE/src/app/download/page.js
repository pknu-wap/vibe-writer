import Link from "next/link";

export default function Download() {
  return (
    <div className="min-h-screen bg-black text-white">
      <header className="flex items-baseline gap-4 px-8 py-6">
        <Link href="/">
          <h1 className="text-3xl font-black tracking-wide hover:opacity-80 transition-opacity cursor-pointer">
            VIBE - WRITER
          </h1>
        </Link>
        <p className="text-sm text-white/70">
          AI 감정 기반 숏폼 자막 자동 생성 서비스
        </p>
      </header>

      <main className="flex items-center justify-center gap-16 px-12 mt-12">
        <div className="flex flex-col items-center gap-2">
          <div className="w-72 aspect-[9/16] bg-white rounded-lg shadow-2xl"></div>
          <p className="text-xs text-white/40">미리보기</p>
        </div>

        <div className="flex-1 max-w-2xl space-y-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center">
              <svg
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
            <h2 className="text-4xl font-black">완성됐어요!</h2>
          </div>

          <div className="flex gap-3 flex-wrap">
            <span className="px-5 py-1.5 rounded-full bg-yellow-400 text-black font-black text-sm">
              happy
            </span>
            <span className="px-5 py-1.5 rounded-full bg-red-500 text-white font-black text-sm">
              Angry
            </span>
            <span className="px-5 py-1.5 rounded-full bg-sky-400 text-white font-black text-sm">
              Sad
            </span>
            <span className="px-5 py-1.5 rounded-full bg-gray-300 text-black font-black text-sm">
              Neutral
            </span>
          </div>

          <button className="w-full py-5 rounded-2xl bg-black border-2 border-white text-white text-xl font-bold hover:bg-white/10 transition-colors cursor-pointer">
            다운로드
          </button>

          <Link href="/edit" className="block">
            <button className="w-full py-5 rounded-2xl bg-white text-black text-xl font-bold hover:bg-white/90 transition-colors cursor-pointer">
              다시 편집하기
            </button>
          </Link>
        </div>
      </main>
    </div>
  );
}
