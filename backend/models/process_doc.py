from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.types import JSON

from database import Base


class ProcessDoc(Base):
    """Reference documents (e.g. bureaucratic process guides) retrieved by the
    explain_process tool. `embedding` holds a plain float vector rather than a
    native pgvector column: the placeholder hashing embedding in
    utils/embeddings.py doesn't need real vector-index search, and this keeps
    the schema installable without the pgvector Postgres extension. Swap to a
    pgvector.sqlalchemy.Vector column once a real embedding model is wired in.
    """

    __tablename__ = "process_docs"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    embedding = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
