from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    title = Column(String)

    subject = Column(String)

    script = Column(String)

    video_path = Column(String)

    thumbnail_path = Column(String)

    duration = Column(Integer, default=0)

    status = Column(String, default="completed")

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")