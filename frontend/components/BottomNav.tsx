import Link from "next/link";

export default function BottomNav({ active }: { active: "home" | "history" | "settings" }) {
  return (
    <div className="bottom-nav">
      <Link href="/home" className={`nav-item ${active === "home" ? "active" : ""}`}>
        <span className="n-icon">🏠</span>Home
      </Link>
      <Link href="/history" className={`nav-item ${active === "history" ? "active" : ""}`}>
        <span className="n-icon">🕘</span>History
      </Link>
      <Link href="/settings" className={`nav-item ${active === "settings" ? "active" : ""}`}>
        <span className="n-icon">⚙️</span>Settings
      </Link>
    </div>
  );
}
