from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from agents.llm import get_llm
from agents.registry import register_tool
from langchain_core.messages import HumanMessage, SystemMessage
from models import User

SYSTEM_PROMPT = """তুমি একজন আর্থিক সহকারী। ব্যবহারকারীর বলা bKash/Nagad/ব্যাংক লেনদেনগুলো বিশ্লেষণ করে \
প্রতিটি লেনদেন সহজ বাংলায় ব্যাখ্যা করো। অপরিচিত নম্বরে বড় Cash Out, একই দিনে বহুবার টাকা পাঠানো, বা \
অস্বাভাবিক প্যাটার্ন থাকলে সেটিকে flagged=true করো এবং একটি সংক্ষিপ্ত সতর্কতা ট্যাগ দাও।"""


class TxnExplain(BaseModel):
    name: str = Field(description="লেনদেনের সংক্ষিপ্ত নাম, যেমন 'Cash Out — Unknown'")
    amount: str = Field(description="যেমন '-৳2,500'")
    note: str = Field(description="সহজ বাংলায় ব্যাখ্যা")
    flagged: bool = False
    tag: str | None = Field(default=None, description="যেমন '⚠ Unusual Activity'")


class StatementExplanation(BaseModel):
    transactions: list[TxnExplain]
    summary_bn: str = Field(description="এক লাইনে মৌখিক সারাংশ, flagged লেনদেন থাকলে তা উল্লেখ করে")


@register_tool("statement_explain")
def run(decision, db: Session, user: User) -> tuple[str, dict | None]:
    statement_text = decision.statement_text
    if not statement_text:
        return "আপনার লেনদেনের বিবরণ ঠিক বুঝতে পারিনি, আবার বলবেন কি?", None

    llm = get_llm().with_structured_output(StatementExplanation)
    result: StatementExplanation = llm.invoke(
        [SystemMessage(content=SYSTEM_PROMPT), HumanMessage(content=statement_text)]
    )

    data = {"transactions": [t.model_dump() for t in result.transactions]}
    return result.summary_bn, data
