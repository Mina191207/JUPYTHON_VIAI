from sqlalchemy.orm import Session

from app.db.models.video import Video


class VideoRecordService:
    def create(
        self,
        db: Session,
        user_id: int,
        task_id: str,
        title: str,
        file_path: str,
        credit_used: int = 0,
        resolution: str | None = None,
        duration: int | None = None,
    ):
        video = Video(
            user_id=user_id,
            task_id=task_id,
            title=title,
            file_path=file_path,
            credit_used=credit_used,
            resolution=resolution,
            duration=duration,
            status="completed",
        )

        db.add(video)
        db.commit()
        db.refresh(video)

        return video


video_record_service = VideoRecordService()