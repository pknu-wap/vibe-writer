const MOCK_SEGMENTS = [
  { text: "아니 어찌됐든 우리는 저 뉴욕을 갔다올테니까", start: 0.0, end: 2.4 },
  {
    text: "여러분들 또 안에서 달력을 또 찍어주시길 바라요",
    start: 2.4,
    end: 5.1,
  },
  { text: "밑에서도 하나 돌리죠 저희", start: 5.1, end: 6.3 },
  { text: "안 해, 안 해, 안 해, 안 해", start: 6.3, end: 8.8 },
  { text: "일단 돌린다", start: 8.8, end: 9.5 },
  { text: "안 해, 안 해, 난 무효", start: 9.5, end: 10.3 },
  { text: "아이 일로 와요", start: 10.3, end: 11.7 },
  { text: "몰라 자기네들끼리 하고 안해", start: 11.7, end: 13.9 },
  { text: "그럼 하지마, 이씨", start: 13.9, end: 15.1 },
  { text: "아니 그걸 왜 그걸 발로 차고 그래요", start: 16.6, end: 19.9 },
  { text: "아 이거 참 새 신발을", start: 19.9, end: 21.9 },
];

const toSrtTime = (sec) => {
  const h = Math.floor(sec / 3600)
    .toString()
    .padStart(2, "0");
  const m = Math.floor((sec % 3600) / 60)
    .toString()
    .padStart(2, "0");
  const s = Math.floor(sec % 60)
    .toString()
    .padStart(2, "0");
  const ms = Math.round((sec % 1) * 1000)
    .toString()
    .padStart(3, "0");
  return `${h}:${m}:${s},${ms}`;
};

const buildSrt = (segments) =>
  segments
    .map(
      (seg, i) =>
        `${i + 1}\n${toSrtTime(seg.start)} --> ${toSrtTime(seg.end)}\n${seg.text}`,
    )
    .join("\n\n");

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const videoId = searchParams.get("video_id");

  if (!videoId) {
    return new Response(JSON.stringify({ error: "video_id is required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  const srt = buildSrt(MOCK_SEGMENTS);

  return new Response(srt, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Content-Disposition": `attachment; filename="subtitles.srt"`,
    },
  });
}
