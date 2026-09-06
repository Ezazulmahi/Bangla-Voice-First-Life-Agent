"use client";

import { useEffect, useState } from "react";

import BackTopBar from "@/components/BackTopBar";
import { listMobilePackages, MobilePackage } from "@/lib/api";
import { readToolResult } from "@/lib/resultStore";
import { useAuthGuard } from "@/lib/useAuthGuard";

interface PackageRow extends MobilePackage {
  best: boolean;
}

const OPERATOR_STYLE: Record<string, { abbr: string; color: string; label: string }> = {
  grameenphone: { abbr: "GP", color: "var(--green)", label: "Grameenphone" },
  robi: { abbr: "Rb", color: "var(--red)", label: "Robi" },
  banglalink: { abbr: "Bl", color: "var(--blue)", label: "Banglalink" },
  airtel: { abbr: "Ar", color: "#8E2DE2", label: "Airtel" },
};

export default function PackagesPage() {
  const token = useAuthGuard();
  const [packages, setPackages] = useState<PackageRow[] | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!token) return;

    const fromVoice = readToolResult<{ packages: PackageRow[] }>("mobile_compare");
    if (fromVoice?.packages?.length) {
      setPackages(fromVoice.packages);
      setLoading(false);
      return;
    }

    listMobilePackages()
      .then((rows) => {
        const sorted = [...rows].sort((a, b) => a.price_bdt - b.price_bdt);
        setPackages(sorted.map((p, i) => ({ ...p, best: i === 0 })));
      })
      .catch(() => setPackages([]))
      .finally(() => setLoading(false));
  }, [token]);

  return (
    <div className="screen">
      <div className="status-bar" />
      <BackTopBar title="Package Compare" rightIcon="🔊" />
      <div className="content">
        <div className="result-header">
          <h2>Best Data Packages</h2>
          <div className="bn-line">সবচেয়ে ভালো ডেটা প্যাকেজসমূহ</div>
        </div>

        {loading && <div className="bn-line">লোড হচ্ছে...</div>}
        {!loading && packages?.length === 0 && <div className="bn-line">কোনো প্যাকেজ পাওয়া যায়নি।</div>}

        {packages?.map((p) => {
          const style = OPERATOR_STYLE[p.operator] || { abbr: p.operator.slice(0, 2), color: "var(--ink-soft)", label: p.operator };
          return (
            <div key={p.id} className={`package-card ${p.best ? "best" : ""}`}>
              {p.best && <div className="best-tag">সেরা মূল্য</div>}
              <div className="op-badge" style={{ background: style.color }}>
                {style.abbr}
              </div>
              <div className="package-info">
                <div className="p-name">{p.name}</div>
                <div className="p-detail">{style.label}</div>
              </div>
              <div className="package-price">৳{p.price_bdt}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
