"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import {
  ApiError,
  getStoredLanguage,
  requestOtp,
  setStoredLanguage,
  setStoredPhone,
  setToken,
  updateMe,
  verifyOtp,
} from "@/lib/api";
import { ensurePushSubscription } from "@/lib/push";

export default function SignInPage() {
  const router = useRouter();
  const [step, setStep] = useState<"phone" | "otp">("phone");
  const [phone, setPhone] = useState("");
  const [code, setCode] = useState("");
  const [debugCode, setDebugCode] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState<"bn" | "en">(getStoredLanguage());

  async function handleSendCode() {
    setError(null);
    if (phone.trim().length < 6) {
      setError("সঠিক ফোন নম্বর দিন");
      return;
    }
    setLoading(true);
    try {
      const res = await requestOtp(phone.trim());
      setDebugCode(res.debug_code);
      setStep("otp");
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "কিছু একটা ভুল হয়েছে");
    } finally {
      setLoading(false);
    }
  }

  async function handleVerify() {
    setError(null);
    if (code.trim().length !== 6) {
      setError("৬ সংখ্যার কোড দিন");
      return;
    }
    setLoading(true);
    try {
      const res = await verifyOtp(phone.trim(), code.trim());
      setToken(res.access_token);
      setStoredPhone(phone.trim());
      await updateMe({ preferred_language: language }).catch(() => {});
      ensurePushSubscription().catch(() => {});
      router.push("/home");
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "কিছু একটা ভুল হয়েছে");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="screen">
      <div className="status-bar" />
      <div className="content">
        <div className="onboard">
          <div className="big-icon">🎙️</div>
          <h1>Sohai</h1>
          <div className="bn-line">আপনার কথা বলা সহকারী</div>

          {step === "phone" ? (
            <>
              <input
                className="phone-input"
                placeholder="01XXX-XXXXXX"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                inputMode="tel"
              />
              <button className="big-btn" onClick={handleSendCode} disabled={loading}>
                {loading ? "..." : "এগিয়ে যান · Continue"}
              </button>
            </>
          ) : (
            <>
              <input
                className="phone-input"
                placeholder="৬ সংখ্যার কোড"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                inputMode="numeric"
                maxLength={6}
              />
              <button className="big-btn" onClick={handleVerify} disabled={loading}>
                {loading ? "..." : "যাচাই করুন · Verify"}
              </button>
              {debugCode && (
                <div className="bn-line" style={{ marginTop: 10, marginBottom: 0 }}>
                  (dev) কোড: {debugCode}
                </div>
              )}
            </>
          )}

          {error && (
            <div className="bn-line" style={{ color: "var(--red)", marginTop: 10, marginBottom: 0 }}>
              {error}
            </div>
          )}

          <div className="lang-toggle">
            <span
              className={language === "bn" ? "active" : ""}
              role="button"
              style={{ cursor: "pointer" }}
              onClick={() => {
                setLanguage("bn");
                setStoredLanguage("bn");
              }}
            >
              বাংলা
            </span>
            <span
              className={language === "en" ? "active" : ""}
              role="button"
              style={{ cursor: "pointer" }}
              onClick={() => {
                setLanguage("en");
                setStoredLanguage("en");
              }}
            >
              English
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
