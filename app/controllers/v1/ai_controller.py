from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.v1.ai_service import ai_service
from app.services.v1.auth_service import get_current_user
from app.db.models.user import User

from app.schemas.script_schema import GenerateScriptRequest
from app.schemas.ai import GenerateSocialMetadataRequest, GenerateSocialMetadataResponse

from app.schemas.ai import (
    EstimateRequest,
    GenerateTermsRequest,
    GenerateTermsResponse,
)

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

@router.post(
    "/generate-terms",
    response_model=GenerateTermsResponse,
)
def generate_terms(
    request: GenerateTermsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ai_service.generate_terms(
        db=db,
        user_id=current_user.id,
        video_subject=request.video_subject,
        video_script=request.video_script,
        amount=request.amount,
        match_script_order=request.match_script_order,
    )

@router.post(
    "/generate-social-metadata",
    response_model=GenerateSocialMetadataResponse,
)
def generate_social_metadata(
    request: GenerateSocialMetadataRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ai_service.generate_social_metadata(
        db=db,
        user_id=current_user.id,
        video_subject=request.video_subject,
        video_script=request.video_script,
    )