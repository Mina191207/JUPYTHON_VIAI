from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.constants.payment import PaymentStatus, PaymentType
from app.db.models.payment import Payment
from app.db.models.payment_method import PaymentMethod
from app.db.models.plan import Plan
from app.db.models.user import User

from app.services.v1.credit_service import credit_service
from app.services.v1.subscription_service import subscription_service

class PaymentService:

    CREDIT_RATE = 1000  # 1000đ = 1 credit

    def create_payment(
        self,
        db: Session,
        user_id: int,
        payment_type: str,
        payment_method_id: int,
        amount: int | None = None,
        plan_id: int | None = None,
    ):

        # ==========================
        # Kiểm tra User
        # ==========================
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )

        # ==========================
        # Kiểm tra Payment Method
        # ==========================
        payment_method = (
            db.query(PaymentMethod)
            .filter(PaymentMethod.id == payment_method_id)
            .first()
        )

        if payment_method is None:
            raise HTTPException(
                status_code=404,
                detail="Payment method not found",
            )

        payment_type = payment_type.upper()

        # ==========================
        # CREDIT
        # ==========================
        if payment_type == PaymentType.CREDIT.value:

            if amount is None:
                raise HTTPException(
                    status_code=400,
                    detail="Amount is required",
                )

            if amount <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid amount",
                )

            credit_added = amount // self.CREDIT_RATE

        # ==========================
        # SUBSCRIPTION
        # ==========================
        elif payment_type == PaymentType.SUBSCRIPTION.value:

            if plan_id is None:
                raise HTTPException(
                    status_code=400,
                    detail="Plan is required",
                )

            plan = (
                db.query(Plan)
                .filter(
                    Plan.id == plan_id,
                    Plan.is_active == True,
                )
                .first()
            )

            if plan is None:
                raise HTTPException(
                    status_code=404,
                    detail="Plan not found",
                )

            amount = plan.price
            credit_added = plan.credit

        else:
            raise HTTPException(
                status_code=400,
                detail="Invalid payment type",
            )

        payment = Payment(
            user_id=user.id,
            plan_id=plan_id,
            payment_method_id=payment_method.id,
            payment_type=payment_type,
            amount=amount,
            credit_added=credit_added,
            status=PaymentStatus.PENDING.value,
)

        db.add(payment)
        db.commit()
        db.refresh(payment)

        return payment
    
    def complete_payment(
        self,
        db: Session,
        payment_id: int,
        user_id: int,
    ):

        payment = (
            db.query(Payment)
            .filter(Payment.id == payment_id)
            .filter(Payment.user_id == user_id)
            .first()
        )

        if payment is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found",
            )

        if payment.status == PaymentStatus.SUCCESS.value:
            raise HTTPException(
                status_code=400,
                detail="Payment already completed",
            )

        try:

            payment.status = PaymentStatus.SUCCESS.value

            credit_service.add_credit(
                db=db,
                user_id=payment.user_id,
                amount=payment.credit_added,
                reason="Payment Success",
            )

            if payment.payment_type == PaymentType.SUBSCRIPTION.value:

                subscription_service.activate_subscription(
                    db=db,
                    user_id=payment.user_id,
                    plan_id=payment.plan_id,
                )

            db.commit()
            db.refresh(payment)

            return payment

        except Exception:
            db.rollback()
            raise


payment_service = PaymentService()