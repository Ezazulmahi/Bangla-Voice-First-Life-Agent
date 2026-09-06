"use client";

import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import BackTopBar from "@/components/BackTopBar";
import { ConversationTurn, getConversationHistory, mediaUrl } from "@/lib/api";
import { useAuthGuard } from "@/lib/useAuthGuard";

export default function ConversationDetailPage() {
  const token = useAuthGuard();
  const params = useParams<{ id: string }>();
  const [turns, setTurns] = useState<ConversationTurn[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!token) return;
    getConversationHistory(Number(params.id))
      .then(setTurns)
      .catch(() => setError("এই কথোপকথনটি খুঁজে পাওয়া যায়নি।"));
  }, [token, params.id]);

  return (
    <div className="screen">
      <div className="status-bar" />
      <BackTopBar title="Conversation" backHref="/history" />
      <div className="content">
        {error && <div className="bn-line">{error}</div>}
        {!error && !turns && <div className="bn-line">লোড হচ্ছে...</div>}
        {turns?.length === 0 && <div className="bn-line">এই কথোপকথনে কিছু নেই।</div>}
        {turns?.map((t) => {
          const audioSrc = mediaUrl(t.audio_file_path);
          return (
            <div key={t.id} className={`transcript-bubble ${t.role === "user" ? "user" : ""}`}>
              <span className="who">{t.role === "user" ? "You" : "Sohai"}</span>
              {audioSrc && (
                <audio controls src={audioSrc} style={{ width: "100%", marginBottom: 6 }} />
              )}
              {t.transcript_text}
            </div>
          );
        })}
      </div>
    </div>
  );
}
