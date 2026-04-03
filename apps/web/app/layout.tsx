import "./globals.css";
import type { ReactNode } from "react";

export const metadata = {
  title: "GEO AI Visibility Console",
  description: "Internal delivery console for AI visibility operations"
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}

