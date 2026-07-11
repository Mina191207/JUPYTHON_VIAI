from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.v1.base import new_router

from app.db.database import get_db
from app.db.models.user import User

from app.schemas.payment import (
    CreatePaymentRequest,
    CreatePaymentResponse,
)

from app.services.v1.auth_service import get_current_user
from app.services.v1.payment_service import payment_service


router = new_router()


@router.post(
    "/payments/create",
    response_model=CreatePaymentResponse,
)
def create_payment(
    request: CreatePaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    payment = payment_service.create_payment(
        db=db,
        user_id=current_user.id,
        payment_type=request.payment_type,
        payment_method_id=request.payment_method_id,
        amount=request.amount,
        plan_id=request.plan_id,
    )

    return {
        "id": payment.id,
        "payment_type": payment.payment_type,
        "amount": payment.amount,
        "credit_added": payment.credit_added,
        "status": payment.status,
    }