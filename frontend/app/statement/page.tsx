"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import BackTopBar from "@/components/BackTopBar";
import { readToolResult } from "@/lib/resultStore";
import { useAuthGuard } from "@/lib/useAuthGuard";

interface Transaction {
  name: string;
  amount: string;
  note: string;
  flagged: boolean;
  tag: string | null;
}

export default function StatementPage() {
  const token = useAuthGuard();
  const [transactions, setTransactions] = useState<Transaction[] | null>(null);

  useEffect(() => {
    if (!token) return;
    const fromVoice = readToolResult<{ transactions: Transaction[] }>("statement_explain");
    setTransactions(fromVoice?.transactions ?? []);
  }, [token]);

  return (
    <div className="screen">
      <div className="status-bar" />
      <BackTopBar title="Statement Explained" rightIcon="🔊" />
      <div className="content">
        <div className="result-header">
          <h2>Your Recent Transactions</h2>
          <div className="bn-line">আপনার সাম্প্রতিক লেনদেন</div>
        </div>

        {transactions?.length === 0 && (
          <div className="bn-line">
            এখনো কোনো লেনদেন ব্যাখ্যা করা হয়নি। হোম থেকে মাইক চেপে আপনার bKash/Nagad লেনদেন বলুন।
            <br />
            <Link href="/home" style={{ textDecoration: "underline" }}>
              হোমে ফিরে যান
            </Link>
          </div>
        )}

        {transactions?.map((t, i) => (
          <div key={i} className={`txn-item ${t.flagged ? "flag" : ""}`}>
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
