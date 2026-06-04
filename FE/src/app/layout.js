import "./globals.css";
export default function RootLayout({ children }) {
  return (
    <html lang="ko">
      <head>
        <link
          rel="stylesheet"
          href="https://api.fontshare.com/v2/css?f[]=nippo@700,900&display=swap"
        />
      </head>

      <body>{children}</body>
    </html>
  );
}