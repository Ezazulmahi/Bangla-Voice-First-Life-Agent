"""Extensible tool registry: adding a new agent capability means writing a
new module under agents/tools/ that calls register_tool(name) — no changes
needed to the router's dispatch logic."""

from typing import Any, Callable

from sqlalchemy.orm import Session

from models import User

# First arg is a RouterDecision (defined in router_agent.py); typed as Any
# here to avoid a circular import between the registry and the router.
ToolFn = Callable[[Any, Session, User], tuple[str, dict | None]]

TOOL_REGISTRY: dict[str, ToolFn] = {}


def register_tool(name: str):
    def decorator(fn: ToolFn) -> ToolFn:
        TOOL_REGISTRY[name] = fn
        return fn

    return decorator
