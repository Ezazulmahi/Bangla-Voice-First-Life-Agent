from sqlalchemy.orm import Session

from agents.registry import register_tool
from models import MobilePackage, User


@register_tool("mobile_compare")
def run(decision, db: Session, user: User) -> tuple[str, dict | None]:
    query = db.query(MobilePackage)
    if decision.max_price:
        query = query.filter(MobilePackage.price_bdt <= decision.max_price)
    packages = query.order_by(MobilePackage.price_bdt.asc()).limit(5).all()

    if not packages:
        return "দুঃখিত, এই মুহূর্তে কোনো মিলে যাওয়া প্যাকেজ পাওয়া যায়নি।", {"packages": []}

    best = packages[0]
    reply = (
        f"{best.operator.value.capitalize()}-এর {best.name} প্যাকেজটি সবচেয়ে ভালো মূল্যে "
        f"— মাত্র ৳{best.price_bdt} টাকা।"
    )
    data = {
        "packages": [
            {
                "id": p.id,
                "operator": p.operator.value,
                "name": p.name,
                "data_gb": float(p.data_gb),
                "validity_days": p.validity_days,
                "price_bdt": float(p.price_bdt),
                "best": p.id == best.id,
            }
            for p in packages
        ]
    }
    return reply, data
