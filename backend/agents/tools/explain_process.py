from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy.orm import Session

from agents.language import language_directive
from agents.llm import get_llm
from agents.registry import register_tool
from models import ProcessDoc, User
from utils.embeddings import cosine_similarity, embed_text

TOP_K = 3

SYSTEM_PROMPT = """তুমি একজন সহকারী যে প্রাতিষ্ঠানিক/সরকারি প্রক্রিয়া সহজ ভাষায় ব্যাখ্যা করো। \
নিচের তথ্যসূত্র (বাংলায় লেখা, কিন্তু তোমাকে প্রয়োজনে অনুবাদ/সারমর্ম করতে হবে) ব্যবহার করে \
ব্যবহারকারীর প্রশ্নের ধাপে ধাপে উত্তর দাও। তথ্যসূত্রে উত্তর না থাকলে সততার সাথে বলো যে নির্দিষ্ট \
তথ্য নেই।"""


def _top_docs(db: Session, question: str) -> list[ProcessDoc]:
    docs = db.query(ProcessDoc).all()
    if not docs:
        return []
    query_vec = embed_text(question)
    scored = sorted(docs, key=lambda d: cosine_similarity(query_vec, d.embedding), reverse=True)
    return scored[:TOP_K]


@register_tool("explain_process")
def run(decision, db: Session, user: User) -> tuple[str, dict | None]:
    lang = user.preferred_language.value
    question = decision.process_question or ""
    top_docs = _top_docs(db, question)

    if not top_docs:
        no_info = {
            "bn": "দুঃখিত, এই বিষয়ে আমার কাছে এখনো কোনো তথ্য নেই।",
            "en": "Sorry, I don't have information on this topic yet.",
        }
        return no_info[lang], {"sources": []}

    context = "\n\n".join(f"### {d.title}\n{d.content}" for d in top_docs)
    llm = get_llm()
    response = llm.invoke(
        [
            SystemMessage(content=f"{SYSTEM_PROMPT}\n\nতথ্যসূত্র:\n{context}" + language_directive(lang)),
            HumanMessage(content=question),
        ]
    )
    reply = response.content.strip()
    data = {"sources": [d.title for d in top_docs]}
    return reply, data
