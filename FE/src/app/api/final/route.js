export async function POST() {
  await new Promise((r) => setTimeout(r, 1000));

  return Response.json({ success: true });
}
