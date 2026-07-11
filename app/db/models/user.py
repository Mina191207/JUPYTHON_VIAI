from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    picture = Column(String(255), nullable=True)

    first_name = Column(String(100), nullable=True)

    last_name = Column(String(100), nullable=True)

    email = Column(String(255), unique=True, nullable=False)

    phone_number = Column(String(20))

    password_hash = Column(String(255), nullable=False)

    role = Column(String(20), default="user", nullable=False)

    credit_balance = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )