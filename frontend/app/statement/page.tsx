import BackTopBar from "@/components/BackTopBar";

const transactions = [
  {
    name: "Cash Out — Unknown",
    amount: "-৳2,500",
    flagged: true,
    note: "এই লেনদেনটি একটি নতুন নম্বরে করা হয়েছে যা আগে কখনো ব্যবহার হয়নি। এটি আপনি না করলে সাথে সাথে বিকাশ হেল্পলাইনে যোগাযোগ করুন।",
    tag: "⚠ Unusual Activity",
  },
  {
    name: "Mobile Recharge",
    amount: "-৳49",
    flagged: false,
    note: "এটি আপনার নিয়মিত মোবাইল রিচার্জ, প্রতি সপ্তাহে একই পরিমাণে হয়ে থাকে।",
  },
  {
    name: "Send Money — Rahim",
    amount: "-৳1,000",
    flagged: false,
    note: "এটি আপনার পূর্বের সংরক্ষিত পরিচিতি রহিমকে পাঠানো টাকা।",
  },
];

export default function StatementPage() {
  return (
    <div className="screen">
      <div className="status-bar" />
      <BackTopBar title="Statement Explained" rightIcon="🔊" />
      <div className="content">
        <div className="result-header">
          <h2>Your Recent Transactions</h2>
          <div className="bn-line">আপনার সাম্প্রতিক লেনদেন</div>
        </div>
        {transactions.map((t) => (
          <div key={t.name} className={`txn-item ${t.flagged ? "flag" : ""}`}>
            <div className="txn-top">
              <span className="t-name">{t.name}</span>
              <span className="t-amt">{t.amount}</span>
            </div>
            <p>{t.note}</p>
            {t.tag && <span className="flag-tag">{t.tag}</span>}
          </div>
        ))}
      </div>
    </div>
  );
}
