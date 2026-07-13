from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String

from app.db.database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    task_id = Column(String(255), nullable=False)

    title = Column(String(255), nullable=False)

    resolution = Column(String(50), nullable=True)

    credit_used = Column(Integer, default=0, nullable=False)

    status = Column(String(50), nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    file_path = Column(String(255), nullable=True)

    duration = Column(Integer, nullable=True)

