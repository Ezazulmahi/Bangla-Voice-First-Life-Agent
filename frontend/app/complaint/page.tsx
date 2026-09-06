"use client";

import { useEffect, useState } from "react";

import BackTopBar from "@/components/BackTopBar";
import { ApiError, ComplaintDraft, createComplaintDraft } from "@/lib/api";
import { readToolResult } from "@/lib/resultStore";
import { useAuthGuard } from "@/lib/useAuthGuard";

interface VoiceDraft {
  draft_id: number;
  company_name: string;
  generated_text: string;
}

export default function ComplaintPage() {
  const token = useAuthGuard();
  const [companyName, setCompanyName] = useState("");
  const [issueDescription, setIssueDescription] = useState("");
  const [draft, setDraft] = useState<{ company_name: string; generated_text: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    const fromVoice = readToolResult<VoiceDraft>("complaint_draft");
    if (fromVoice) {
      setDraft({ company_name: fromVoice.company_name, generated_text: fromVoice.generated_text });
    }
  }, [token]);

  async function handleGenerate() {
    setError(null);
    if (!companyName.trim() || !issueDescription.trim()) {
      setError("কোম্পানির নাম এবং সমস্যার বিবরণ দিন");
      return;
    }
    setLoading(true);
    try {
      const result: ComplaintDraft = await createComplaintDraft(companyName.trim(), issueDescription.trim());
      setDraft({ company_name: result.company_name, generated_text: result.generated_text });
    } catch (e) {
      setError(e instanceof ApiError ? e.message : "কিছু একটা ভুল হয়েছে");
    } finally {
      setLoading(false);
    }
  }

  function handleEdit() {
    setDraft(null);
  }

  function handleSendNotice() {
    setNotice("এই ফিচারটি শীঘ্রই আসছে — এখন শুধু চিঠিটি কপি করে নিজে পাঠাতে পারেন।");
  }

  return (
    <div className="screen">
      <div className="status-bar" />
      <BackTopBar title="Complaint Ready" rightIcon="🔊" />
      <div className="content">
        <div className="result-header">
          <h2>{draft ? "Your Complaint is Ready" : "Draft a Complaint"}</h2>
          <div className="bn-line">
            {draft ? "আপনার অভিযোগপত্র তৈরি হয়েছে" : "কোম্পানির নাম ও সমস্যার বিবরণ দিন"}
          </div>
        </div>

        {draft ? (
          <>
            <div className="draft-box">
              <div className="label">Draft to: {draft.company_name}</div>
              <p>{draft.generated_text}</p>
            </div>
            <div className="send-options">
              <button className="send-btn sms" onClick={handleSendNotice}>
                📱 SMS পাঠান
              </button>
              <button className="send-btn email" onClick={handleSendNotice}>
                ✉️ ইমেইল পাঠান
              </button>
            </div>
            <button className="edit-link" onClick={handleEdit}>
              পরিবর্তন করতে চাপুন · Edit this draft
            </button>
            {notice && (
              <div className="bn-line" style={{ marginTop: 10 }}>
                {notice}
              </div>
            )}
          </>
        ) : (
          <>
            <input
              className="phone-input"
              placeholder="কোম্পানির নাম · Company name"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
            />
            <textarea
              className="phone-input"
              placeholder="সমস্যার বিবরণ · Issue description"
              value={issueDescription}
              onChange={(e) => setIssueDescription(e.target.value)}
              rows={5}
              style={{ resize: "vertical", textAlign: "left" }}
            />
            <button className="big-btn" onClick={handleGenerate} disabled={loading}>
              {loading ? "..." : "তৈরি করুন · Generate"}
            </button>
            {error && (
              <div className="bn-line" style={{ color: "var(--red)", marginTop: 10 }}>
                {error}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
