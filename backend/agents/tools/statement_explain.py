from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from agents.language import language_directive
from agents.llm import get_llm
from agents.registry import register_tool
from langchain_core.messages import HumanMessage, SystemMessage
from models import User

SYSTEM_PROMPT = """তুমি একজন আর্থিক সহকারী। ব্যবহারকারীর বলা bKash/Nagad/ব্যাংক লেনদেনগুলো বিশ্লেষণ করে \
প্রতিটি লেনদেন সহজ ভাষায় ব্যাখ্যা করো। অপরিচিত নম্বরে বড় Cash Out, একই দিনে বহুবার টাকা পাঠানো, বা \
অস্বাভাবিক প্যাটার্ন থাকলে সেটিকে flagged=true করো এবং একটি সংক্ষিপ্ত সতর্কতা ট্যাগ দাও। স্বাভাবিক, \
নিয়মিত লেনদেনকে (যেমন পরিচিত পরিচিতিকে টাকা পাঠানো, নিয়মিত রিচার্জ) flagged=false রাখো — সবকিছু flag \
কোরো না।"""


class TxnExplain(BaseModel):
    name: str = Field(description="short transaction name, e.g. 'Cash Out — Unknown'")
    amount: str = Field(description="e.g. '-৳2,500'")
    note: str = Field(description="plain-language explanation, in the requested output language")
    flagged: bool = False
    tag: str | None = Field(default=None, description="e.g. '⚠ Unusual Activity', in the requested language")


class StatementExplanation(BaseModel):
    transactions: list[TxnExplain]
    summary: str = Field(description="one-line spoken summary, mentioning flagged transactions if any")


@register_tool("statement_explain")
def run(decision, db: Session, user: User) -> tuple[str, dict | None]:
    lang = user.preferred_language.value
    statement_text = decision.statement_text
    if not statement_text:
        unclear = {
            "bn": "আপনার লেনদেনের বিবরণ ঠিক বুঝতে পারিনি, আবার বলবেন কি?",
            "en": "I couldn't quite make out your transaction details — could you say them again?",
        }
        return unclear[lang], None

    llm = get_llm().with_structured_output(StatementExplanation)
    result: StatementExplanation = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT + language_directive(lang)),
            HumanMessage(content=statement_text),
        ]
    )

    data = {"transactions": [t.model_dump() for t in result.transactions]}
    return result.summary, data
