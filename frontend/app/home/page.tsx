"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import BottomNav from "@/components/BottomNav";
import BrandTopBar from "@/components/BrandTopBar";
import { getMe } from "@/lib/api";
import { useAuthGuard } from "@/lib/useAuthGuard";

export default function HomePage() {
  const token = useAuthGuard();
  const [phone, setPhone] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    getMe()
      .then((user) => setPhone(user.phone_number))
      .catch(() => {});
  }, [token]);

  return (
    <div className="screen">
      <div className="status-bar" />
      <BrandTopBar />
      <div className="content">
        <div className="greeting">
          <h1>Hi{phone ? `, ${phone}` : ""}</h1>
          <div className="bn-line">আজ আপনাকে কীভাবে সাহায্য করতে পারি?</div>
        </div>
        <div className="mic-zone">
          <Link href="/listening" className="mic-btn">
            🎙️
          </Link>
          <div className="mic-hint">বলতে চাপুন · Tap to speak</div>
        </div>
        <div className="task-grid">
          <Link href="/packages" className="task-tile">
            <div className="t-icon" style={{ background: "var(--blue)" }}>
              📶
            </div>
            <div className="t-title">Mobile Packages</div>
            <div className="t-bn">মোবাইল প্যাকেজ</div>
          </Link>
          <Link href="/statement" className="task-tile">
            <div className="t-icon" style={{ background: "var(--green)" }}>
              💳
            </div>
            <div className="t-title">Explain Statement</div>
            <div className="t-bn">লেনদেন বুঝুন</div>
          </Link>
          <Link href="/complaint" className="task-tile">
            <div className="t-icon" style={{ background: "var(--red)" }}>
              📝
            </div>
            <div className="t-title">Draft Complaint</div>
            <div className="t-bn">অভিযোগ লিখুন</div>
          </Link>
          <Link href="/history" className="task-tile">
            <div className="t-icon" style={{ background: "var(--yellow)", color: "var(--ink)" }}>
              ⏰
            </div>
            <div className="t-title">Reminders</div>
            <div className="t-bn">রিমাইন্ডার</div>
          </Link>
        </div>
      </div>
      <BottomNav active="home" />
    </div>
  );
}
