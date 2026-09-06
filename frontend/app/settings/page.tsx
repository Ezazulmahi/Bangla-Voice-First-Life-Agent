"use client";

import { useEffect, useState } from "react";

import BottomNav from "@/components/BottomNav";
import BrandTopBar from "@/components/BrandTopBar";
import { getMe, Me, updateMe } from "@/lib/api";
import { useAuthGuard } from "@/lib/useAuthGuard";

export default function SettingsPage() {
  const token = useAuthGuard();
  const [me, setMe] = useState<Me | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!token) return;
    getMe().then(setMe).catch(() => {});
  }, [token]);

  async function setLanguage(lang: "bn" | "en") {
    if (!me || me.preferred_language === lang) return;
    setSaving(true);
    setMe({ ...me, preferred_language: lang });
    try {
      await updateMe({ preferred_language: lang });
    } catch {
      setMe(me); // revert on failure
    } finally {
      setSaving(false);
    }
  }

  async function toggleAudioRetention() {
    if (!me) return;
    const next = !me.audio_retention_opt_in;
    setMe({ ...me, audio_retention_opt_in: next });
    try {
      await updateMe({ audio_retention_opt_in: next });
    } catch {
      setMe(me);
    }
  }

  return (
    <div className="screen">
      <div className="status-bar" />
      <BrandTopBar />
      <div className="content">
        <div className="section-title">Settings · সেটিংস</div>

        {me && (
          <>
            <div className="task-tile" style={{ textAlign: "left", marginBottom: 12 }}>
              <div className="t-title" style={{ marginBottom: 8 }}>
                Agent Language · এজেন্টের ভাষা
              </div>
              <div className="lang-toggle" style={{ marginTop: 0 }}>
                <span
                  className={me.preferred_language === "bn" ? "active" : ""}
                  role="button"
                  style={{ cursor: "pointer" }}
                  onClick={() => setLanguage("bn")}
                >
                  বাংলা
                </span>
                <span
                  className={me.preferred_language === "en" ? "active" : ""}
                  role="button"
                  style={{ cursor: "pointer" }}
                  onClick={() => setLanguage("en")}
                >
                  English
                </span>
              </div>
            </div>

            <div className="reminder-card">
              <div className="reminder-icon">🎙️</div>
              <div className="reminder-info">
                <div className="r-title">Save my voice recordings</div>
                <div className="r-date">আমার ভয়েস রেকর্ডিং সংরক্ষণ করুন</div>
              </div>
              <button
                className="toggle"
                aria-label="Toggle audio retention"
                onClick={toggleAudioRetention}
                style={{ background: me.audio_retention_opt_in ? "var(--green)" : "var(--line)" }}
              />
            </div>
          </>
        )}

        {!me && <div className="bn-line">লোড হচ্ছে...</div>}
      </div>
      <BottomNav active="settings" />
    </div>
  );
}
