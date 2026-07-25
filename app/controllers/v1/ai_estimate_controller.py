from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User
from app.schemas.ai import EstimateRequest
from app.services.v1.ai_service import ai_service
from app.services.v1.auth_service import get_current_user

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/estimate")
def estimate(
    request: EstimateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return ai_service.estimate(
        db=db,
        user_id=current_user.id,
        video_subject=request.video_subject,
        language=request.language,
        paragraph_number=request.paragraph_number,
    )