from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy.orm import Session

from agents.language import language_directive
from agents.llm import get_llm
from agents.registry import register_tool
from models import ComplaintDraft, User

SYSTEM_PROMPT = """তুমি একজন সহকারী যে গ্রাহকের হয়ে প্রাতিষ্ঠানিক অভিযোগপত্র/অনুরোধপত্র লিখে দাও। \
নিচের কোম্পানির নাম ও সমস্যার বিবরণ থেকে একটি সংক্ষিপ্ত, ভদ্র কিন্তু দৃঢ় অভিযোগপত্র লেখো। \
শুধু চিঠির মূল অংশ লেখো, কোনো বাড়তি ব্যাখ্যা ছাড়া।"""


def generate_text(company_name: str, issue_description: str, lang: str = "bn") -> str:
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT + language_directive(lang)),
            HumanMessage(content=f"Company: {company_name}\nIssue: {issue_description}"),
        ]
    )
    return response.content.strip()


def generate_and_save(
    db: Session,
    user_id: int,
    company_name: str,
    issue_description: str,
    conversation_turn_id: int | None = None,
    lang: str = "bn",
) -> ComplaintDraft:
    generated_text = generate_text(company_name, issue_description, lang)
    draft = ComplaintDraft(
        user_id=user_id,
        conversation_turn_id=conversation_turn_id,
        company_name=company_name,
        issue_description=issue_description,
        generated_text=generated_text,
    )
    db.add(draft)
    db.commit()
    db.refresh(draft)
    return draft


@register_tool("complaint_draft")
def run(decision, db: Session, user: User) -> tuple[str, dict | None]:
    lang = user.preferred_language.value
    company_name = decision.company_name or "the concerned company"
    issue_description = decision.issue_description or ""
    draft = generate_and_save(db, user.id, company_name, issue_description, lang=lang)
    reply = {"bn": "আপনার অভিযোগপত্র তৈরি হয়েছে।", "en": "Your complaint letter is ready."}[lang]
    data = {
        "draft_id": draft.id,
        "company_name": draft.company_name,
        "generated_text": draft.generated_text,
    }
    return reply, data
