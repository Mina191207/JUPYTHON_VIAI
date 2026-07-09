from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.database import Base


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(50),
        nullable=False,
        unique=True,
    )

    icon = Column(String(255))

    provider = Column(
        String(50),
        nullable=False,
    )

    description = Column(
        String(255),
    )

    is_active = Column(
        Boolean,
        default=True,
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