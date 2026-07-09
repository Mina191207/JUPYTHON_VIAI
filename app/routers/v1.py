from fastapi import APIRouter

from app.controllers.v1.credit_controller import router as credit_router
from app.controllers.v1.video import router as video_router
from app.controllers.v1.llm import router as llm_router

router = APIRouter()

router.include_router(credit_router)
router.include_router(video_router)
router.include_router(llm_router)