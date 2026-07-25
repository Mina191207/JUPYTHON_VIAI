from fastapi import APIRouter

from app.controllers.v1.credit_controller import router as credit_router
from app.controllers.v1.video import router as video_router
from app.controllers.v1.llm import router as llm_router
from app.controllers.v1.auth import auth as auth_router
from app.controllers.v1.payment_controller import router as payment_router
from app.controllers.v1.plan_controller import router as plan_router
from app.controllers.v1.vnpay_controller import router as vnpay_router
from app.controllers.v1.ai_provider_controller import router as ai_provider_router
from app.controllers.v1.ai_controller import router as ai_router
from app.controllers.v1.ai_estimate_controller import router as estimate_router

router = APIRouter()

router.include_router(credit_router)
#router.include_router(video_router)
#router.include_router(llm_router)
router.include_router(auth_router)
router.include_router(payment_router)
router.include_router(plan_router)
router.include_router(vnpay_router)
router.include_router(ai_provider_router)
router.include_router(ai_router)
router.include_router(estimate_router)