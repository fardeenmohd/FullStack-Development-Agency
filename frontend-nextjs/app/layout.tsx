import "./globals.css";
export const metadata = { title: "Lead Hunter", description: "B2B Platform" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
