import BackTopBar from "@/components/BackTopBar";

export default function ComplaintPage() {
  return (
    <div className="screen">
      <div className="status-bar" />
      <BackTopBar title="Complaint Ready" rightIcon="🔊" />
      <div className="content">
        <div className="result-header">
          <h2>Your Complaint is Ready</h2>
          <div className="bn-line">আপনার অভিযোগপত্র তৈরি হয়েছে</div>
        </div>
        <div className="draft-box">
          <div className="label">Draft to: Daraz Customer Support</div>
          <p>
            প্রিয় দারাজ কর্তৃপক্ষ, আমি গত ২৮ আগস্ট একটি পণ্য অর্ডার করেছিলাম (অর্ডার নং ৪৪৫২১) যা এখনো পৌঁছায়নি।
            ডেলিভারির নির্ধারিত সময় পার হয়ে গেছে ৫ দিন। অনুগ্রহ করে দ্রুত ব্যবস্থা নিন অথবা সম্পূর্ণ টাকা ফেরত দিন।
          </p>
        </div>
        <div className="send-options">
          <button className="send-btn sms">📱 SMS পাঠান</button>
          <button className="send-btn email">✉️ ইমেইল পাঠান</button>
        </div>
        <button className="edit-link">পরিবর্তন করতে চাপুন · Edit this draft</button>
      </div>
    </div>
  );
}
