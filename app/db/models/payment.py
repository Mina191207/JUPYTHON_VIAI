from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.db.database import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    plan_id = Column(Integer, ForeignKey("plans.id"))

    payment_method_id = Column(Integer,ForeignKey("payment_methods.id"),nullable=False,)

    amount = Column(Float)

    credit_added = Column(Integer)

    status = Column(String(30))

    transaction_id = Column(String(255), unique=True)

    created_at = Column(DateTime, default=datetime.utcnow)