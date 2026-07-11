from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.v1.base import new_router
from app.db.database import get_db

from app.schemas.plan import PlanResponse

from app.services.v1.plan_service import plan_service

router = new_router()


@router.get(
    "/plans",
    response_model=list[PlanResponse],
)
def get_plans(
    db: Session = Depends(get_db),
):

    return plan_service.get_all(db)