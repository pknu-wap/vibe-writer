const BACKEND_URL = process.env.BACKEND_URL || "http://localhost:8000";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const videoId = searchParams.get("video_id");

  if (!videoId) {
    return Response.json({ error: "video_id required" }, { status: 400 });
  }

  try {
    const response = await fetch(
      `${BACKEND_URL}/download-ass?video_id=${videoId}`
    );
    const text = await response.text();

    return new Response(text, {
      status: response.status,
      headers: {
        "Content-Type": "text/plain; charset=utf-8",
        "Content-Disposition": `attachment; filename="vibe_writer_${videoId}.ass"`,
      },
    });
  } catch (error) {
    return Response.json(
      { error: "Backend unreachable", message: error.message },
      { status: 500 }
    );
  }
}