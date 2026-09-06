import Link from "next/link";

export default function SignInPage() {
  return (
    <div className="screen">
      <div className="status-bar" />
      <div className="content">
        <div className="onboard">
          <div className="big-icon">🎙️</div>
          <h1>Sohai</h1>
          <div className="bn-line">আপনার কথা বলা সহকারী</div>
          <input className="phone-input" placeholder="01XXX-XXXXXX" />
          <Link href="/home" className="big-btn">
            এগিয়ে যান · Continue
          </Link>
          <div className="lang-toggle">
            <span className="active">বাংলা</span>
            <span>English</span>
          </div>
        </div>
      </div>
    </div>
  );
}
