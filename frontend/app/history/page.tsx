import BrandTopBar from "@/components/BrandTopBar";
import BottomNav from "@/components/BottomNav";

const reminders = [
  { icon: "💡", title: "DESCO Bill Due", date: "Tomorrow · আগামীকাল" },
  { icon: "📶", title: "Data Package Expires", date: "In 2 days · ২ দিনে" },
];

const history = [
  { text: "মোবাইল প্যাকেজ খুঁজেছেন", time: "2h ago" },
  { text: "বিকাশ লেনদেন বুঝেছেন", time: "Yesterday" },
  { text: "দারাজে অভিযোগ পাঠিয়েছেন", time: "2 days ago" },
];

export default function HistoryPage() {
  return (
    <div className="screen">
      <div className="status-bar" />
      <BrandTopBar />
      <div className="content">
        <div className="section-title">Upcoming Reminders · রিমাইন্ডার</div>
        {reminders.map((r) => (
          <div key={r.title} className="reminder-card">
            <div className="reminder-icon">{r.icon}</div>
            <div className="reminder-info">
              <div className="r-title">{r.title}</div>
              <div className="r-date">{r.date}</div>
            </div>
            <button className="toggle" aria-label={`Toggle ${r.title}`} />
          </div>
        ))}

        <div className="section-title">Recent Conversations · সাম্প্রতিক কথোপকথন</div>
        {history.map((h) => (
          <div key={h.text} className="history-item">
            <span className="h-text">{h.text}</span>
            <span className="h-time">{h.time}</span>
          </div>
        ))}
      </div>
      <BottomNav active="history" />
    </div>
  );
}
