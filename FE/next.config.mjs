/** @type {import('next').NextConfig} */
const isProd = process.env.NODE_ENV === "production";
const repo = "vibe-writer";
const basePath = isProd ? `/${repo}` : "";

const nextConfig = {
  output: "export",
  basePath: isProd ? `/${repo}` : "",
  assetPrefix: isProd ? `/${repo}/` : "",
  trailingSlash: true,
  images: { unoptimized: true },
  reactCompiler: true,
  env: {
    NEXT_PUBLIC_BASE_PATH: basePath,
  },
};

export default nextConfig;
