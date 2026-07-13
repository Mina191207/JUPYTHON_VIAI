from typing import Optional

from pydantic import BaseModel

from app.constants.payment import PaymentType

from datetime import datetime


class CreatePaymentRequest(BaseModel):
    payment_type: PaymentType
    payment_method_id: int

    amount: int | None = None

    plan_id: int | None = None


class CreatePaymentResponse(BaseModel):
    id: int
    payment_type: PaymentType
    amount: int
    credit_added: int
    status: str


class PaymentResponse(BaseModel):
    id: int
    payment_type: str
    amount: int
    credit_added: int
    status: str
    transaction_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class PaymentSuccessResponse(BaseModel):
    message: str