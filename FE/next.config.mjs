/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === "production";
const repo = "vibe-writer";

const nextConfig = {
  output: "export",
  basePath: isProd ? `/${repo}` : "",
  assetPrefix: isProd ? `/${repo}/` : "",
  trailingSlash: true,
  images: { unoptimized: true },
  reactCompiler: true,
};

export default nextConfig;
