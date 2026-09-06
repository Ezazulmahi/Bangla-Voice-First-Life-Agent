from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Literal, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from agents.llm import get_llm
from agents.registry import TOOL_REGISTRY
from models import User

# Import tool modules for their register_tool side effects.
from agents.tools import (  # noqa: F401
    complaint_draft,
    explain_process,
    mobile_compare,
    set_reminder,
    statement_explain,
)

ToolChoice = Literal[
    "mobile_compare",
    "statement_explain",
    "complaint_draft",
    "set_reminder",
    "explain_process",
    "none",
]


class RouterDecision(BaseModel):
    tool: ToolChoice = Field(description="Which tool best serves the user's request, or 'none'")

    # mobile_compare
    query: Optional[str] = Field(default=None, description="e.g. '3GB 7 days data package'")
    max_price: Optional[float] = Field(default=None, description="max price in BDT, if mentioned")

    # statement_explain
    statement_text: Optional[str] = Field(
        default=None, description="the transaction lines the user described, verbatim"
    )

    # complaint_draft
    company_name: Optional[str] = None
    issue_description: Optional[str] = None

    # set_reminder
    reminder_title: Optional[str] = None
    reminder_message: Optional[str] = None
    due_at: Optional[str] = Field(
        default=None, description="ISO 8601 datetime, resolved from relative phrases like 'tomorrow'"
    )

    # explain_process
    process_question: Optional[str] = None

    reply_bn: str = Field(
        description="A short, natural spoken reply in Bangla acknowledging the request "
        "(used verbatim if tool is 'none', otherwise the tool's own reply takes over)"
    )


@dataclass
class RouterResult:
    tool_used: str | None
    reply_text: str
    data: dict | None


SYSTEM_PROMPT = """তুমি Sohai — একটি বাংলা ভয়েস-ফার্স্ট সহকারী। ব্যবহারকারীর কথার উপর ভিত্তি করে \
নিচের ৫টি টুলের মধ্যে সবচেয়ে উপযুক্তটি বেছে নাও, অথবা কোনোটিই উপযুক্ত না হলে 'none' বেছে নিয়ে \
নিজেই সংক্ষেপে বাংলায় উত্তর দাও।

Tools:
- mobile_compare: মোবাইল ডেটা/ইন্টারনেট প্যাকেজ তুলনা করতে চাইলে
- statement_explain: bKash/Nagad/ব্যাংক লেনদেন বা স্টেটমেন্ট ব্যাখ্যা করতে চাইলে
- complaint_draft: কোনো কোম্পানির বিরুদ্ধে অভিযোগ বা অনুরোধপত্র লিখতে চাইলে
- set_reminder: বিল, অ্যাপয়েন্টমেন্ট বা কাজের জন্য রিমাইন্ডার সেট করতে চাইলে
- explain_process: কোনো সরকারি/প্রাতিষ্ঠানিক প্রক্রিয়া (যেমন NID সংশোধন) সম্পর্কে জানতে চাইলে

বর্তমান সময় (UTC): {now}. আপেক্ষিক তারিখ (যেমন "আগামীকাল") থেকে due_at একটি ISO 8601 timestamp \
হিসেবে হিসাব করো।"""


def route(transcript: str, user: User, db: Session) -> RouterResult:
    llm = get_llm().with_structured_output(RouterDecision)
    now = datetime.now(timezone.utc).isoformat()
    decision: RouterDecision = llm.invoke(
        [
            SystemMessage(content=SYSTEM_PROMPT.format(now=now)),
            HumanMessage(content=transcript),
        ]
    )

    if decision.tool == "none" or decision.tool not in TOOL_REGISTRY:
        return RouterResult(tool_used=None, reply_text=decision.reply_bn, data=None)

    tool_fn = TOOL_REGISTRY[decision.tool]
    reply_text, data = tool_fn(decision, db, user)
    return RouterResult(tool_used=decision.tool, reply_text=reply_text, data=data)
