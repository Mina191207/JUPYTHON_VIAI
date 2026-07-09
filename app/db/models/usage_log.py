from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.db.database import Base


class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    credit_transaction_id = Column(
    Integer,
    ForeignKey("credit_transactions.id"),
    nullable=True,
)

    provider_id = Column(
    Integer,
    ForeignKey("ai_providers.id"),
    nullable=False,
)

    model = Column(String(100))

    prompt_tokens = Column(Integer)

    completion_tokens = Column(Integer)

    total_tokens = Column(Integer)

    cost = Column(Float)

    credit_used = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)