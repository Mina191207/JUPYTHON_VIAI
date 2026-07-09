from fastapi import Depends
from sqlalchemy.orm import Session

from app.controllers.v1.base import new_router
from app.db.database import get_db
from app.schemas.credit import (
    AddCreditRequest,
    CreditResponse,
)
from app.services.v1.credit_service import credit_service

router = new_router()


@router.post(
    "/credit/add",
    response_model=CreditResponse,
)
def add_credit(
    user_id: int,
    request: AddCreditRequest,
    db: Session = Depends(get_db),
):

    balance = credit_service.add_credit(
        db=db,
        user_id=user_id,
        amount=request.amount,
        reason=request.reason,
    )

    return CreditResponse(balance=balance)


@router.post(
    "/credit/deduct",
    response_model=CreditResponse,
)
def deduct_credit(
    user_id: int,
    request: AddCreditRequest,
    db: Session = Depends(get_db),
):

    balance = credit_service.deduct_credit(
        db=db,
        user_id=user_id,
        amount=request.amount,
        reason=request.reason,
    )

    return CreditResponse(balance=balance)


@router.get(
    "/credit/balance",
    response_model=CreditResponse,
)
def get_balance(
    user_id: int,
    db: Session = Depends(get_db),
):

    balance = credit_service.get_balance(
        db,
        user_id,
    )

    return CreditResponse(balance=balance)