import { createReadStream, statSync } from "fs";
import { join } from "path";
import { Readable } from "stream";

// 목 서버: video_id와 무관하게 sample.mp4를 스트리밍
export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const videoId = searchParams.get("video_id");

  if (!videoId) {
    return Response.json({ error: "video_id is required" }, { status: 400 });
  }

  const filePath = join(process.cwd(), "public", "input.mp4");
  const { size } = statSync(filePath);
  const range = request.headers.get("range");

  if (range) {
    const [startStr, endStr] = range.replace(/bytes=/, "").split("-");
    const start = parseInt(startStr, 10) || 0;
    const end = endStr ? parseInt(endStr, 10) : size - 1;

    return new Response(
      Readable.toWeb(createReadStream(filePath, { start, end })),
      {
        status: 206,
        headers: {
          "Content-Range": `bytes ${start}-${end}/${size}`,
          "Accept-Ranges": "bytes",
          "Content-Length": String(end - start + 1),
          "Content-Type": "video/mp4",
          "Content-Disposition": `attachment; filename="vibe_writer_${videoId}.mp4"`,
        },
      },
    );
  }

  return new Response(Readable.toWeb(createReadStream(filePath)), {
    headers: {
      "Content-Length": String(size),
      "Content-Type": "video/mp4",
      "Accept-Ranges": "bytes",
      "Content-Disposition": `attachment; filename="vibe_writer_${videoId}.mp4"`,
    },
  });
}
