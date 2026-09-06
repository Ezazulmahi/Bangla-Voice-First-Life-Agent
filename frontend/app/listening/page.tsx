"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import {
  ApiError,
  AudioTurnResult,
  createConversation,
  getStoredConversationId,
  mediaUrl,
  setStoredConversationId,
  submitAudio,
} from "@/lib/api";
import { routeForTool, storeToolResult, StorableTool } from "@/lib/resultStore";
import { useAuthGuard } from "@/lib/useAuthGuard";

const bars = [14, 32, 48, 24, 40, 18, 36];

type Stage = "preparing" | "recording" | "processing" | "result" | "error";

export default function ListeningPage() {
  const token = useAuthGuard();
  const router = useRouter();

  const [stage, setStage] = useState<Stage>("preparing");
  const [errorMsg, setErrorMsg] = useState("");
  const [result, setResult] = useState<AudioTurnResult | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (!token) return;
    startRecording();
    return () => {
      mediaRecorderRef.current?.stream.getTracks().forEach((t) => t.stop());
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [token]);

  async function startRecording() {
    setErrorMsg("");
    setResult(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      chunksRef.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      recorder.onstop = handleRecordingStopped;
      mediaRecorderRef.current = recorder;
      recorder.start();
      setStage("recording");
    } catch {
      setErrorMsg("মাইক্রোফোন অনুমতি পাওয়া যায়নি। ব্রাউজার সেটিংসে অনুমতি দিন।");
      setStage("error");
    }
  }

  function stopRecording() {
    mediaRecorderRef.current?.stop();
    mediaRecorderRef.current?.stream.getTracks().forEach((t) => t.stop());
    setStage("processing");
  }

  async function handleRecordingStopped() {
    const blob = new Blob(chunksRef.current, { type: mediaRecorderRef.current?.mimeType || "audio/webm" });
    try {
      let conversationId = getStoredConversationId();
      if (!conversationId) {
        const conversation = await createConversation();
        conversationId = conversation.id;
        setStoredConversationId(conversationId);
      }
      const res = await submitAudio(conversationId, blob);
      setResult(res);
      setStage("result");
      if (res.reply_audio_url) {
        setTimeout(() => audioRef.current?.play().catch(() => {}), 100);
      }
    } catch (e) {
      setErrorMsg(e instanceof ApiError ? e.message : "কিছু একটা ভুল হয়েছে, আবার চেষ্টা করুন।");
      setStage("error");
    }
  }

  function handleMicTap() {
    if (stage === "recording") {
      stopRecording();
    } else if (stage === "error" || stage === "result") {
      startRecording();
    }
  }

  function handleViewDetails() {
    if (!result?.tool_used || !result.data) return;
    const dest = routeForTool(result.tool_used);
    if (!dest) return;
    storeToolResult(result.tool_used as StorableTool, result.data);
    router.push(dest);
  }

  const detailRoute = result?.tool_used ? routeForTool(result.tool_used) : null;
  const replyAudioSrc = mediaUrl(result?.reply_audio_url);

  return (
    <div className="screen">
      <div className="status-bar" />
      <div className="topbar-app">
        <Link href="/home" className="icon-btn" aria-label="Back">
          ←
        </Link>
        <div className="brand">
          <div className="name" style={{ fontSize: 15 }}>
            {stage === "recording" ? "কথা বলছে..." : stage === "processing" ? "ভাবছি..." : "Sohai"}
          </div>
        </div>
        <Link href="/home" className="icon-btn" aria-label="Close">
          ✕
        </Link>
      </div>
      <div className="content listen-wrap">
        {stage !== "error" && (
          <>
            <div className="listen-status">
              {stage === "preparing" && "প্রস্তুত হচ্ছে..."}
              {stage === "recording" && "শুনছি..."}
              {stage === "processing" && "ভাবছি..."}
              {stage === "result" && "সম্পন্ন"}
            </div>
            {(stage === "recording" || stage === "processing") && (
              <div className="waveform">
                {bars.map((h, i) => (
                  <span key={i} style={{ height: h }} />
                ))}
              </div>
            )}
          </>
        )}

        {stage === "error" && (
          <div className="transcript-bubble" style={{ color: "var(--red)" }}>
            {errorMsg}
          </div>
        )}

        {result && (
          <>
            <div className="transcript-bubble user">
              <span className="who">You</span>
              {result.transcript}
            </div>
            <div className="transcript-bubble">
              <span className="who">Sohai</span>
              {replyAudioSrc && (
                <span
                  className="play-icon"
                  role="button"
                  onClick={() => audioRef.current?.play().catch(() => {})}
                  style={{ cursor: "pointer" }}
                >
                  ▶
                </span>
              )}
              {result.reply_text}
            </div>
            {replyAudioSrc && <audio ref={audioRef} src={replyAudioSrc} />}
          </>
        )}

        <div style={{ flex: 1 }} />

        {stage === "result" && detailRoute ? (
          <button className="big-btn" onClick={handleViewDetails} style={{ marginBottom: 16 }}>
            বিস্তারিত দেখুন · View details
          </button>
        ) : null}

        {stage !== "processing" && stage !== "preparing" && (
          <div className="mic-zone" style={{ marginBottom: 6 }}>
            <button
              className="mic-btn"
              style={{
                width: 64,
                height: 64,
                fontSize: 26,
                background: stage === "recording" ? "var(--red)" : "var(--blue)",
              }}
              onClick={handleMicTap}
            >
              🎙️
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
