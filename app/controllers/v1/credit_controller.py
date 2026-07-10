from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.v1.base import new_router
from app.db.database import get_db
from app.db.models.user import User

from app.schemas.credit import (
    AddCreditRequest,
    CreditResponse,
    CreditBalanceResponse,
)

from app.services.v1.auth_service import get_current_user
from app.services.v1.credit_service import credit_service

router = new_router()


@router.get(
    "/credit/balance",
    response_model=CreditBalanceResponse,
)
def get_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    result = credit_service.get_balance(
        db=db,
        user_id=current_user.id,
    )

    return result


@router.post(
    "/credit/add",
    response_model=CreditResponse,
)
def add_credit(
    request: AddCreditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return credit_service.add_credit(
        db=db,
        user_id=current_user.id,
        amount=request.amount,
        reason=request.reason,
    )


@router.post(
    "/credit/deduct",
    response_model=CreditResponse,
)
def deduct_credit(
    request: AddCreditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return credit_service.deduct_credit(
        db=db,
        user_id=current_user.id,
        amount=request.amount,
        reason=request.reason,
    )


@router.get("/credit/history")
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return credit_service.get_history(
        db=db,
        user_id=current_user.id,
    )