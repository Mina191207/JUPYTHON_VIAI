from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

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
        default="active",
        nullable=False,
    )

    start_date = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    end_date = Column(DateTime)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )