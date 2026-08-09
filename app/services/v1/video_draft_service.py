from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.video_draft import VideoDraft


class VideoDraftService:

    MAX_REGENERATE = 3

    def create(
        self,
        db: Session,
        user_id: int,
        video_subject: str,
        script: str,
    ):
        draft = VideoDraft(
            user_id=user_id,
            video_subject=video_subject,
            script=script,
            regenerate_count=0,
        )

        db.add(draft)
        db.commit()
        db.refresh(draft)

        return draft

    def get_by_id(
        self,
        db: Session,
        draft_id: int,
        user_id: int,
    ):
        draft = (
            db.query(VideoDraft)
            .filter(
                VideoDraft.id == draft_id,
                VideoDraft.user_id == user_id,
            )
            .first()
        )

        if not draft:
            raise HTTPException(
                status_code=404,
                detail="Video draft not found",
            )

        return draft

    def update_script(
        self,
        db: Session,
        draft: VideoDraft,
        script: str,
    ):
        draft.script = script

        db.commit()
        db.refresh(draft)

        return draft

    def check_can_regenerate(
        self,
        draft: VideoDraft,
    ):
        if draft.regenerate_count >= self.MAX_REGENERATE:
            raise HTTPException(
                status_code=400,
                detail="Bạn đã sử dụng hết 3 lần tạo lại kịch bản.",
            )

    def increment_regenerate(
        self,
        db: Session,
        draft: VideoDraft,
    ):
        self.check_can_regenerate(draft)

        draft.regenerate_count += 1

        db.commit()
        db.refresh(draft)

        return draft
    
    def regenerate(
        self,
        db: Session,
        draft_id: int,
        user_id: int,
        script: str,
    ):
        draft = self.get_by_id(
            db=db,
            draft_id=draft_id,
            user_id=user_id,
        )

        self.check_can_regenerate(draft)

        draft.script = script
        draft.regenerate_count += 1

        db.commit()
        db.refresh(draft)

        return draft

video_draft_service = VideoDraftService()