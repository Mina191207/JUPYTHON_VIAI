from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from app.db.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)

    description = Column(String(255))

    is_active = Column(Boolean,default=True,)

    price = Column(Float, nullable=False)

    credit = Column(Integer, nullable=False)

    duration_days = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )