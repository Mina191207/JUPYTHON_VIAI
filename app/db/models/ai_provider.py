from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.db.database import Base


class AIProvider(Base):
    __tablename__ = "ai_providers"

    id = Column(Integer, primary_key=True, index=True)

    # Tên hiển thị
    name = Column(
        String(100),
        nullable=False,
    )

    # openai, gemini, groq...
    provider = Column(
        String(50),
        nullable=False,
    )

    # gpt-4o, gemini-2.5-pro...
    model = Column(
        String(100),
        nullable=False,
    )

    # API Key của hệ thống
    api_key = Column(
        String(255),
        nullable=False,
    )

    # Endpoint (nếu cần)
    base_url = Column(
        String(255),
    )

    is_active = Column(
        Boolean,
        default=True,
    )

    # Độ ưu tiên nếu có nhiều API cùng model
    priority = Column(
        Integer,
        default=1,
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