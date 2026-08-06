from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.plan import Plan
from app.db.models.subscription import Subscription


class SubscriptionService:
    def _get_or_create_subscription(self, db: Session, user_id: int):
        subscription = (
            db.query(Subscription)
            .filter(Subscription.user_id == user_id)
            .first()
        )

        if subscription is None:
            subscription = Subscription(user_id=user_id, status="ACTIVE")
            db.add(subscription)
            db.flush()

        return subscription

    def activate_subscription(
        self,
        db: Session,
        user_id: int,
        plan_id: int,
    ):

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

        subscription = self._get_or_create_subscription(db, user_id)

        now = datetime.utcnow()
        end_date = now + timedelta(days=plan.duration_days)

        subscription.plan_id = plan.id
        subscription.status = "ACTIVE"
        subscription.start_date = now
        subscription.renewal_date = now
        subscription.end_date = end_date
        subscription.auto_renew = False

        db.commit()
        db.refresh(subscription)

        return subscription

    def get_active_subscription(
        self,
        db: Session,
        user_id: int,
    ):

        now = datetime.utcnow()

        return (
            db.query(Subscription)
            .filter(
                Subscription.user_id == user_id,
                Subscription.status == "ACTIVE",
                Subscription.end_date > now,
            )
            .first()
        )

    def get_remaining_credit(
        self,
        db: Session,
        user_id: int,
    ):

        subscription = self.get_active_subscription(
            db,
            user_id,
        )

        if subscription is None:
            return 0

        return (
            subscription.total_credit
            - subscription.used_credit
        )

    def use_subscription_credit(
        self,
        db: Session,
        user_id: int,
        credit: int,
    ):

        subscription = self.get_active_subscription(
            db,
            user_id,
        )

        if subscription is None:
            return False

        remaining = (
            subscription.total_credit
            - subscription.used_credit
        )

        if remaining < credit:
            return False

        subscription.used_credit += credit

        db.commit()
        db.refresh(subscription)

        return True

    def renew_subscription(
        self,
        db: Session,
        user_id: int,
    ):

        subscription = self.get_active_subscription(
            db,
            user_id,
        )

        if subscription is None:
            raise HTTPException(
                status_code=404,
                detail="Subscription not found",
            )

        plan = (
            db.query(Plan)
            .filter(
                Plan.id == subscription.plan_id
            )
            .first()
        )

        if plan is None:
            raise HTTPException(
                status_code=404,
                detail="Plan not found",
            )

        now = datetime.utcnow()

        subscription.renewal_date = now
        subscription.end_date = (
            now + timedelta(days=plan.duration_days)
        )

        subscription.total_credit = plan.credit
        subscription.used_credit = 0

        db.commit()
        db.refresh(subscription)

        return subscription

    def get_subscription_info(
        self,
        db: Session,
        user_id: int,
    ):

        subscription = self.get_active_subscription(
            db,
            user_id,
        )

        if subscription is None:
            return None

        return {
            "plan_id": subscription.plan.id,
            "plan_name": subscription.plan.name,
            "status": subscription.status,
            "purchase_date": subscription.start_date,
            "renewal_date": subscription.renewal_date,
            "expire_date": subscription.end_date,
            "total_credit": subscription.total_credit,
            "used_credit": subscription.used_credit,
            "remaining_credit": (
                subscription.total_credit
                - subscription.used_credit
            ),
        }
    def get_current_subscription(
        self,
        db: Session,
        user_id: int,
    ):

        subscription = self.get_active_subscription(
            db=db,
            user_id=user_id,
        )

        if subscription is None:
            return None

        return {
            "plan_id": subscription.plan.id,
            "plan_name": subscription.plan.name,
            "status": subscription.status,
            "start_date": subscription.start_date,
            "renewal_date": subscription.renewal_date,
            "end_date": subscription.end_date,
            "credit_balance": subscription.user.credit_balance,
        }


subscription_service = SubscriptionService()