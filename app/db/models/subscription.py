from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    plan_id = Column(
        Integer,
        ForeignKey("plans.id"),
        nullable=False,
    )

    status = Column(
        String(20),
        default="ACTIVE",
        nullable=False,
    )

    start_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    renewal_date = Column(
        DateTime,
        nullable=True,
    )

    end_date = Column(
        DateTime,
        nullable=False,
    )

    auto_renew = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    user = relationship("User")
    plan = relationship("Plan")