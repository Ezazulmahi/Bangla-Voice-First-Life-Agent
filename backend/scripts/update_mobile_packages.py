"""Manually refresh mobile_packages from a JSON file you maintain.

There's no live data source for this: Bangladeshi operators don't publish a
public pricing API, and scraping their sites/apps raises ToS questions this
project won't resolve unilaterally. Instead, this script is the update path
— check prices yourself (operator app, USSD, customer care, official site)
periodically, edit a JSON file, and run this.

Usage:
    venv/Scripts/python.exe -m scripts.update_mobile_packages path/to/packages.json [--replace-all]

JSON format — a list of objects:
    [
      {"operator": "grameenphone", "name": "3GB · 7 days", "data_gb": 3, "validity_days": 7, "price_bdt": 49},
      ...
    ]
operator must be one of: grameenphone, robi, banglalink, airtel

Existing rows are matched by (operator, name) and updated in place (bumping
updated_at); rows with no match are inserted. Pass --replace-all to also
delete existing packages not present in the file (use when an operator has
discontinued a package).
"""

import argparse
import json
import sys
from datetime import datetime, timezone

from database import SessionLocal
from models import MobilePackage, Operator


def load_entries(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        entries = json.load(f)
    for e in entries:
        if e["operator"] not in Operator.__members__:
            raise ValueError(f"Unknown operator '{e['operator']}' — must be one of {list(Operator.__members__)}")
    return entries


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("json_path")
    parser.add_argument("--replace-all", action="store_true", help="delete packages not present in the file")
    args = parser.parse_args()

    entries = load_entries(args.json_path)
    db = SessionLocal()
    try:
        seen_ids = set()
        updated, inserted = 0, 0
        for e in entries:
            existing = (
                db.query(MobilePackage)
                .filter(MobilePackage.operator == e["operator"], MobilePackage.name == e["name"])
                .first()
            )
            if existing:
                existing.data_gb = e["data_gb"]
                existing.validity_days = e["validity_days"]
                existing.price_bdt = e["price_bdt"]
                existing.updated_at = datetime.now(timezone.utc)
                seen_ids.add(existing.id)
                updated += 1
            else:
                row = MobilePackage(
                    operator=Operator(e["operator"]),
                    name=e["name"],
                    data_gb=e["data_gb"],
                    validity_days=e["validity_days"],
                    price_bdt=e["price_bdt"],
                )
                db.add(row)
                db.flush()
                seen_ids.add(row.id)
                inserted += 1

        removed = 0
        if args.replace_all:
            stale = db.query(MobilePackage).filter(MobilePackage.id.notin_(seen_ids)).all()
            removed = len(stale)
            for row in stale:
                db.delete(row)

        db.commit()
        print(f"updated {updated}, inserted {inserted}, removed {removed}")
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
