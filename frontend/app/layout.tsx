import type { Metadata } from "next";
import { Baloo_2, Hind_Siliguri, Inter } from "next/font/google";
import "./globals.css";
import ReminderNudger from "@/components/ReminderNudger";

const baloo = Baloo_2({
  subsets: ["latin"],
  weight: ["500", "600", "700", "800"],
  variable: "--font-baloo",
});

const hindSiliguri = Hind_Siliguri({
  subsets: ["latin", "bengali"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-hind",
});

const inter = Inter({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Sohai — আপনার কথা বলা সহকারী",
  description: "A Bangla voice-first AI agent that gets things done.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="bn">
      <body className={`${baloo.variable} ${hindSiliguri.variable} ${inter.variable}`}>
        <ReminderNudger />
        {children}
      </body>
    </html>
  );
}
