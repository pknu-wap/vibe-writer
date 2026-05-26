const MOCK_SEGMENTS = [
  {
    text: "아니 어찌됐든 우리는 저 뉴욕을 갔다올테니까",
    start: 0.0,
    end: 2.4,
    emotion: "Neutral",
  },
  {
    text: "여러분들 또 안에서 달력을 또 찍어주시길 바라요",
    start: 2.4,
    end: 5.1,
    emotion: "Happy",
  },
  {
    text: "밑에서도 하나 돌리죠 저희",
    start: 5.1,
    end: 6.3,
    emotion: "Neutral",
  },
  {
    text: "안 해, 안 해, 안 해, 안 해",
    start: 6.3,
    end: 8.8,
    emotion: "Angry",
  },
  { text: "일단 돌린다", start: 8.8, end: 9.5, emotion: "Neutral" },
  { text: "안 해, 안 해, 난 무효", start: 9.5, end: 10.3, emotion: "Angry" },
  { text: "아이 일로 와요", start: 10.3, end: 11.7, emotion: "Angry" },
  {
    text: "몰라 자기네들끼리 하고 안해",
    start: 11.7,
    end: 13.9,
    emotion: "Sad",
  },
  { text: "그럼 하지마, 이씨", start: 13.9, end: 15.1, emotion: "Angry" },
  {
    text: "아니 그걸 왜 그걸 발로 차고 그래요",
    start: 16.6,
    end: 19.9,
    emotion: "Angry",
  },
  { text: "아 이거 참 새 신발을", start: 19.9, end: 21.9, emotion: "Sad" },
];

export async function POST(request) {
  const { video_id } = await request.json();

  if (!video_id) {
    return Response.json({ error: "video_id is required" }, { status: 400 });
  }

  await new Promise((r) => setTimeout(r, 1000));

  return Response.json({ video_id, segments: MOCK_SEGMENTS });
}
