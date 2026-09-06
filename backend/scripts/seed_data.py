"""Seed reference data: mobile packages (for compare_prices) and process docs
(for explain_process's RAG retrieval). Safe to re-run — skips if already seeded.

Usage: venv/Scripts/python.exe -m scripts.seed_data
"""

from database import SessionLocal
from models import MobilePackage, Operator, ProcessDoc
from utils.embeddings import embed_text

MOBILE_PACKAGES = [
    (Operator.grameenphone, "3GB · 7 days", 3, 7, 49),
    (Operator.robi, "3GB · 7 days", 3, 7, 58),
    (Operator.banglalink, "3GB · 6 days", 3, 6, 54),
    (Operator.airtel, "3GB · 7 days", 3, 7, 62),
]

PROCESS_DOCS = [
    (
        "জাতীয় পরিচয়পত্র (NID) সংশোধন প্রক্রিয়া",
        "জাতীয় পরিচয়পত্রে ভুল তথ্য সংশোধনের জন্য প্রথমে services.nidw.gov.bd ওয়েবসাইটে লগইন করে "
        "'তথ্য সংশোধন' অপশনে আবেদন করতে হবে। নাম, জন্ম তারিখ বা ঠিকানার প্রমাণস্বরূপ সংশ্লিষ্ট কাগজপত্র "
        "(জন্ম নিবন্ধন সনদ, শিক্ষা সনদ, ইউটিলিটি বিল ইত্যাদি) স্ক্যান করে আপলোড করতে হবে। আবেদন ফি "
        "বিকাশ/নগদের মাধ্যমে পরিশোধ করা যায়। সংশোধনের ধরন অনুযায়ী সাধারণত ১৫-৩০ কার্যদিবস সময় লাগে। "
        "আবেদনের অবস্থা একই ওয়েবসাইটে ট্র্যাকিং নম্বর দিয়ে দেখা যায়।",
    ),
    (
        "জন্ম নিবন্ধন সনদ উত্তোলন প্রক্রিয়া",
        "জন্ম নিবন্ধন সনদের জন্য bdris.gov.bd ওয়েবসাইটে অনলাইনে আবেদন করতে হয়। প্রয়োজনীয় তথ্যের মধ্যে "
        "শিশুর নাম, জন্ম তারিখ, পিতামাতার জাতীয় পরিচয়পত্র নম্বর ও স্থায়ী ঠিকানা উল্লেখ করতে হয়। "
        "আবেদনের পর নির্ধারিত ফি পরিশোধ করে সংশ্লিষ্ট স্থানীয় সরকার কার্যালয় (ইউনিয়ন পরিষদ/পৌরসভা/সিটি "
        "কর্পোরেশন) থেকে মূল সনদ সংগ্রহ করতে হয়। সাধারণত ৭-১৫ কার্যদিবসের মধ্যে সনদ প্রস্তুত হয়ে যায়।",
    ),
    (
        "মোবাইল ব্যাংকিং (bKash/Nagad) হিসাব থেকে অভিযোগ দায়েরের প্রক্রিয়া",
        "অননুমোদিত লেনদেন বা প্রতারণার শিকার হলে সাথে সাথে bKash হেল্পলাইন (16247) বা Nagad হেল্পলাইনে "
        "(16167) কল করে হিসাব সাময়িকভাবে বন্ধ (ব্লক) করার অনুরোধ জানাতে হবে। এরপর নিকটস্থ থানায় সাধারণ "
        "ডায়েরি (জিডি) করে লেনদেনের প্রমাণ (এসএমএস, লেনদেন নম্বর) সংরক্ষণ করতে হবে। অভিযোগের কপি নিয়ে "
        "সংশ্লিষ্ট মোবাইল ব্যাংকিং প্রতিষ্ঠানের গ্রাহক সেবা কেন্দ্রে লিখিত অভিযোগ জমা দিলে তদন্ত শুরু হয়।",
    ),
]


def seed_mobile_packages(db):
    if db.query(MobilePackage).count() > 0:
        print("mobile_packages already seeded, skipping")
        return
    for operator, name, data_gb, validity_days, price_bdt in MOBILE_PACKAGES:
        db.add(
            MobilePackage(
                operator=operator,
                name=name,
                data_gb=data_gb,
                validity_days=validity_days,
                price_bdt=price_bdt,
            )
        )
    db.commit()
    print(f"seeded {len(MOBILE_PACKAGES)} mobile packages")


def seed_process_docs(db):
    if db.query(ProcessDoc).count() > 0:
        print("process_docs already seeded, skipping")
        return
    for title, content in PROCESS_DOCS:
        db.add(ProcessDoc(title=title, content=content, embedding=embed_text(f"{title}\n{content}")))
    db.commit()
    print(f"seeded {len(PROCESS_DOCS)} process docs")


def main():
    db = SessionLocal()
    try:
        seed_mobile_packages(db)
        seed_process_docs(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
