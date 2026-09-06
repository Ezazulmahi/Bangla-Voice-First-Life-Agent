import Link from "next/link";

const bars = [14, 32, 48, 24, 40, 18, 36];

export default function ListeningPage() {
  return (
    <div className="screen">
      <div className="status-bar" />
      <div className="topbar-app">
        <Link href="/home" className="icon-btn" aria-label="Back">
          ←
        </Link>
        <div className="brand">
          <div className="name" style={{ fontSize: 15 }}>
            কথা বলছে...
          </div>
        </div>
        <Link href="/home" className="icon-btn" aria-label="Close">
          ✕
        </Link>
      </div>
      <div className="content listen-wrap">
        <div className="listen-status">শুনছি...</div>
        <div className="waveform">
          {bars.map((h, i) => (
            <span key={i} style={{ height: h }} />
          ))}
        </div>
        <div className="transcript-bubble user">
          <span className="who">You</span>
          আমার জন্য সবচেয়ে ভালো মোবাইল ডেটা প্যাকেজ কোনটা?
        </div>
        <div className="transcript-bubble">
          <span className="who">Sohai</span>
          <span className="play-icon">▶</span>
          গ্রামীণফোনের ৩জিবি ৭ দিনের প্যাকেজটি সবচেয়ে ভালো মূল্যে — মাত্র ৪৯ টাকা। আমি আপনাকে বিস্তারিত দেখাচ্ছি।
        </div>
        <div style={{ flex: 1 }} />
        <div className="mic-zone" style={{ marginBottom: 6 }}>
          <Link
            href="/packages"
            className="mic-btn"
            style={{ width: 64, height: 64, fontSize: 26, background: "var(--blue)" }}
          >
            🎙️
          </Link>
        </div>
      </div>
    </div>
  );
}
