from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import Conversation, TurnRole, User
from schemas.conversation import ConversationOut, ConversationTurnOut

router = APIRouter(prefix="/conversations", tags=["conversations"])


def get_owned_conversation(conversation_id: int, user: User, db: Session) -> Conversation:
    conversation = db.get(Conversation, conversation_id)
    if conversation is None or conversation.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conversation not found")
    return conversation


@router.post("", response_model=ConversationOut)
def create_conversation(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    conversation = Conversation(user_id=current_user.id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


@router.get("", response_model=list[ConversationOut])
def list_conversations(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.created_at.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )
    result = []
    for c in conversations:
        agent_turns = [t for t in c.turns if t.role == TurnRole.agent]
        last_agent_turn = agent_turns[-1] if agent_turns else None
        result.append(
            ConversationOut(
                id=c.id,
                created_at=c.created_at,
                last_transcript=last_agent_turn.transcript_text if last_agent_turn else None,
                last_tool_used=(
                    last_agent_turn.tool_used.value
                    if last_agent_turn and last_agent_turn.tool_used
                    else None
                ),
            )
        )
    return result


@router.get("/{conversation_id}/history", response_model=list[ConversationTurnOut])
def get_history(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = get_owned_conversation(conversation_id, current_user, db)
    return conversation.turns
