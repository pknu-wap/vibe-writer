export async function POST() {
  await new Promise((r) => setTimeout(r, 1000));
  return Response.json({
    video_id: "vid_20260515_153022",
    duration: 21.94,
    filename: "input.mp4",
    size_mb: 1.0,
  });
}
