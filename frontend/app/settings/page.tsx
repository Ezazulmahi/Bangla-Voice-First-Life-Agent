import BrandTopBar from "@/components/BrandTopBar";
import BottomNav from "@/components/BottomNav";

export default function SettingsPage() {
  return (
    <div className="screen">
      <div className="status-bar" />
      <BrandTopBar />
      <div className="content">
        <div className="section-title">Settings · সেটিংস</div>
        <div className="bn-line">শীঘ্রই আসছে...</div>
      </div>
      <BottomNav active="settings" />
    </div>
  );
}
