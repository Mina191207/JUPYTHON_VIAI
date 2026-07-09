from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.db.database import Base


class CreditTransaction(Base):
    __tablename__ = "credit_transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)

    type = Column(String(30), nullable=False)

    amount = Column(Integer, nullable=False)

    balance_before = Column(Integer)

    balance_after = Column(Integer)

    description = Column(String(255))

    created_at = Column(DateTime, default=datetime.utcnow)