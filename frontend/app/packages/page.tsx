import BackTopBar from "@/components/BackTopBar";

const packages = [
  { op: "GP", color: "var(--green)", name: "3GB · 7 days", detail: "Grameenphone", price: "৳49", best: true },
  { op: "Rb", color: "var(--red)", name: "3GB · 7 days", detail: "Robi", price: "৳58", best: false },
  { op: "Bl", color: "var(--blue)", name: "3GB · 6 days", detail: "Banglalink", price: "৳54", best: false },
  { op: "Ar", color: "#8E2DE2", name: "3GB · 7 days", detail: "Airtel", price: "৳62", best: false },
];

export default function PackagesPage() {
  return (
    <div className="screen">
      <div className="status-bar" />
      <BackTopBar title="Package Compare" rightIcon="🔊" />
      <div className="content">
        <div className="result-header">
          <h2>Best Data Packages</h2>
          <div className="bn-line">সবচেয়ে ভালো ডেটা প্যাকেজসমূহ</div>
        </div>
        {packages.map((p) => (
          <div key={p.op} className={`package-card ${p.best ? "best" : ""}`}>
            {p.best && <div className="best-tag">সেরা মূল্য</div>}
            <div className="op-badge" style={{ background: p.color }}>
              {p.op}
            </div>
            <div className="package-info">
              <div className="p-name">{p.name}</div>
              <div className="p-detail">{p.detail}</div>
            </div>
            <div className="package-price">{p.price}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
