from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.v1.ai_service import ai_service
from app.services.v1.auth_service import get_current_user

from app.schemas.script_schema import GenerateScriptRequest

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)

@router.post("/generate-script")
def generate_script(
    request: GenerateScriptRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):

    return ai_service.generate_script(
        db=db,
        user_id=user.id,
        video_subject=request.video_subject,
        language=request.language,
        paragraph_number=request.paragraph_number,
    )