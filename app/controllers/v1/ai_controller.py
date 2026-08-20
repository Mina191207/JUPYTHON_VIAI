import threading
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import SessionLocal, get_db
from app.models import const
from app.models.schema import VideoAspect
from app.services import state as sm
from app.services.v1.ai_service import ai_service
from app.services.v1.auth_service import get_current_user
from app.services.v1.video_draft_service import video_draft_service
from app.db.models.user import User

from app.schemas.script_schema import GenerateScriptRequest

from app.schemas.ai import (
    EstimateRequest,
    GenerateScriptResponse,
    GenerateTermsRequest,
    GenerateTermsResponse,
    GenerateSocialMetadataRequest,
    GenerateSocialMetadataResponse,
    GenerateVideoRequest,
    GenerateVideoTask,
    RegenerateScriptRequest,
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
        charge_credit=False,
    )

@router.post(
    "/regenerate-script",
    response_model=GenerateScriptResponse,
)
def regenerate_script(
    request: RegenerateScriptRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ai_service.regenerate_script(
        db=db,
        user_id=current_user.id,
        draft_id=request.draft_id,
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

@router.post(
    "/generate-video",
    response_model=GenerateVideoTask,
)
def generate_video(
    request: GenerateVideoRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bắt đầu tạo video nền và trả về ngay task_id.

    FE sẽ poll GET /ai/generate-video/{task_id} để lấy tiến trình thực tế.
    """
    draft = video_draft_service.get_by_id(
        db=db,
        draft_id=request.draft_id,
        user_id=current_user.id,
    )
    if not draft:
        raise HTTPException(status_code=404, detail="Draft not found")

    task_id = str(uuid.uuid4())
    user_id = current_user.id
    sm.state.update_task(
        task_id,
        state=const.TASK_STATE_PROCESSING,
        progress=0,
    )

    options = request.model_dump()
    # model_dump() chuyển VideoAspect enum thành chuỗi ("9:16"...).
    # Downstream gọi .to_resolution() nên phải khôi phục lại enum.
    options["video_aspect"] = VideoAspect(options["video_aspect"])

    def _run():
        task_db = SessionLocal()
        try:
            ai_service.generate_video(
                db=task_db,
                user_id=user_id,
                task_id=task_id,
                **options,
            )
        finally:
            task_db.close()

    threading.Thread(target=_run, daemon=True).start()

    return {
        "task_id": task_id,
        "state": const.TASK_STATE_PROCESSING,
        "progress": 0,
    }


@router.get(
    "/generate-video/{task_id}",
    response_model=GenerateVideoTask,
)
def get_generate_video_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
):
    """Trả về tiến trình của tác vụ tạo video đang chạy nền.

    task_id là UUID ngẫu nhiên nên không cần check ownership (giống endpoint
    legacy /tasks/{task_id}); MemoryState.update_task ghi đè toàn bộ dict nên
    không thể lưu thêm field như user_id ở đây.
    """
    task = sm.state.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {
        "task_id": task.get("task_id", task_id),
        "state": task.get("state", const.TASK_STATE_PROCESSING),
        "progress": task.get("progress", 0),
        "result": task.get("result"),
        "error": task.get("error"),
    }