"use client";

import { useEffect, useState } from "react";

import BottomNav from "@/components/BottomNav";
import BrandTopBar from "@/components/BrandTopBar";
import { ConversationSummary, listConversations, listReminders, Reminder, updateReminder } from "@/lib/api";
import { useAuthGuard } from "@/lib/useAuthGuard";

const TOOL_ICON: Record<string, string> = {
  mobile_compare: "📶",
  statement_explain: "💳",
  complaint_draft: "📝",
  set_reminder: "⏰",
  explain_process: "📄",
};

const TOOL_LABEL: Record<string, string> = {
  mobile_compare: "মোবাইল প্যাকেজ খুঁজেছেন",
  statement_explain: "লেনদেন বুঝেছেন",
  complaint_draft: "অভিযোগ লিখেছেন",
  set_reminder: "রিমাইন্ডার সেট করেছেন",
  explain_process: "প্রক্রিয়া জেনেছেন",
};

// For timestamps already in the past (conversations).
function formatPast(iso: string): string {
  const diffHrs = Math.round((Date.now() - new Date(iso).getTime()) / 3_600_000);
  if (diffHrs < 1) return "এইমাত্র";
  if (diffHrs < 24) return `${diffHrs}h ago`;
  const diffDays = Math.round(diffHrs / 24);
  if (diffDays === 1) return "Yesterday";
  return `${diffDays} days ago`;
}

// For due dates, which are normally in the future (reminders).
function formatDue(iso: string): string {
  const diffHrs = Math.round((new Date(iso).getTime() - Date.now()) / 3_600_000);
  if (diffHrs < 0) return "মেয়াদোত্তীর্ণ · Overdue";
  if (diffHrs < 1) return "এখনই · Now";
  if (diffHrs < 24) return `${diffHrs}h · ${diffHrs} ঘণ্টায়`;
  const diffDays = Math.round(diffHrs / 24);
  if (diffDays === 1) return "Tomorrow · আগামীকাল";
  return `In ${diffDays} days · ${diffDays} দিনে`;
}

export default function HistoryPage() {
  const token = useAuthGuard();
  const [reminders, setReminders] = useState<Reminder[]>([]);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;
    Promise.all([
      listReminders().then(setReminders).catch(() => setReminders([])),
      listConversations().then(setConversations).catch(() => setConversations([])),
    ]).finally(() => setLoading(false));
  }, [token]);

  async function toggleReminder(r: Reminder) {
    setReminders((prev) => prev.map((x) => (x.id === r.id ? { ...x, enabled: !x.enabled } : x)));
    try {
      await updateReminder(r.id, { enabled: !r.enabled });
    } catch {
      setReminders((prev) => prev.map((x) => (x.id === r.id ? { ...x, enabled: r.enabled } : x)));
    }
  }

  const withSummary = conversations.filter((c) => c.last_tool_used);

  return (
    <div className="screen">
      <div className="status-bar" />
      <BrandTopBar />
      <div className="content">
        <div className="section-title">Upcoming Reminders · রিমাইন্ডার</div>
        {loading && <div className="bn-line">লোড হচ্ছে...</div>}
        {!loading && reminders.length === 0 && <div className="bn-line">কোনো রিমাইন্ডার নেই।</div>}
        {reminders.map((r) => (
          <div key={r.id} className="reminder-card">
            <div className="reminder-icon">⏰</div>
            <div className="reminder-info">
              <div className="r-title">{r.title}</div>
              <div className="r-date">{formatDue(r.due_at)}</div>
            </div>
            <button
              className="toggle"
              aria-label={`Toggle ${r.title}`}
              onClick={() => toggleReminder(r)}
              style={{ background: r.enabled ? "var(--green)" : "var(--line)" }}
            />
          </div>
        ))}

        <div className="section-title">Recent Conversations · সাম্প্রতিক কথোপকথন</div>
        {!loading && withSummary.length === 0 && <div className="bn-line">এখনো কোনো কথোপকথন নেই।</div>}
        {withSummary.map((c) => (
          <div key={c.id} className="history-item">
            <span className="h-text">
              {c.last_tool_used ? `${TOOL_ICON[c.last_tool_used] ?? ""} ${TOOL_LABEL[c.last_tool_used] ?? c.last_tool_used}` : ""}
            </span>
            <span className="h-time">{formatPast(c.created_at)}</span>
          </div>
        ))}
      </div>
      <BottomNav active="history" />
    </div>
  );
}
