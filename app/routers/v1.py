from fastapi import APIRouter

from app.controllers.v1.credit_controller import router as credit_router
from app.controllers.v1.video import router as video_router
from app.controllers.v1.llm import router as llm_router
from app.controllers.v1.auth import auth as auth_router
from app.controllers.v1.payment_controller import router as payment_router
from app.controllers.v1.plan_controller import router as plan_router

router = APIRouter()

router.include_router(credit_router)
router.include_router(video_router)
router.include_router(llm_router)
router.include_router(auth_router)
router.include_router(payment_router)
router.include_router(plan_router)