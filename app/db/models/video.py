from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    task_id = Column(String(255), unique=True, nullable=False)

    title = Column(String(255))

    subject = Column(String(255))

    script = Column(String)

    file_path = Column(String(500))

    thumbnail_path = Column(String(500))

    duration = Column(Integer, default=0)

    resolution = Column(String(50))

    credit_used = Column(Integer, default=0)

    status = Column(String(50), default="completed")

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")