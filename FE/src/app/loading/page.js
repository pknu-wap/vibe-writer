import Link from "next/link";

export default function Loading() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#1a0033] to-black">
      <header className="flex items-baseline gap-4 px-8 py-6">
        <Link href="/">
          <h1 className="text-3xl font-black tracking-wide text-white hover:opacity-80 transition-opacity cursor-pointer">
            VIBE - WRITER
          </h1>
        </Link>
        <p className="text-sm text-white/80">
          AI 감정 기반 숏폼 자막 자동 생성 서비스
        </p>
      </header>

      <div className="flex items-center justify-center mt-12">
        <div className="w-[600px] aspect-square rounded-3xl border border-white/40 bg-gradient-to-b from-zinc-700/70 to-zinc-900/80 shadow-2xl">
          <div className="flex flex-col items-center justify-center h-full px-12 gap-10">
            <span className="loading loading-spinner w-24 h-24 text-white"></span>

            <p className="text-xl text-white text-center">
              AI가 감정을 분석하고 자막을 생성하는 중이에요
            </p>

            <div className="w-full">
              <progress
                className="progress w-full"
                value="60"
                max="100"
              ></progress>
              <p className="text-sm text-white/70 text-center mt-3">
                stt 변환 중 ... 60%
              </p>
            </div>
          </div>
        </div>
      </div>

      <Link
        href="/edit"
        className="fixed bottom-4 right-4 px-3 py-1.5 rounded-md bg-yellow-500/20 border border-yellow-500/40 text-xs text-yellow-200 hover:bg-yellow-500/30 transition-colors"
      >
        [debug] /edit →
      </Link>
    </div>
  );
}
