from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException

from app.controllers.v1.base import new_router

from app.db.database import get_db

from app.db.models.user import User

from app.services.v1.auth_service import get_current_user

from app.schemas.subscription import CurrentSubscriptionResponse

from app.services.v1.subscription_service import subscription_service


router = APIRouter(prefix="", tags=["User"])

@router.get(
    "/current-subscription",
    response_model=CurrentSubscriptionResponse,
)
def get_current_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    subscription = subscription_service.get_current_subscription(
        db=db,
        user_id=current_user.id,
    )

    if subscription is None:
        raise HTTPException(
            status_code=404,
            detail="No active subscription",
        )

    return subscription