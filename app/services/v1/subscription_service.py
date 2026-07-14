from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.plan import Plan
from app.db.models.subscription import Subscription


class SubscriptionService:

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

        subscription = (
            db.query(Subscription)
            .filter(Subscription.user_id == user_id)
            .first()
        )

        start_date = datetime.utcnow()
        end_date = start_date + timedelta(days=plan.duration_days)

        if subscription:
            subscription.plan_id = plan.id
            subscription.start_date = start_date
            subscription.end_date = end_date
            subscription.status = "ACTIVE"
        else:
            subscription = Subscription(
                user_id=user_id,
                plan_id=plan.id,
                start_date=start_date,
                end_date=end_date,
                status="ACTIVE",
            )

            db.add(subscription)

        return subscription


subscription_service = SubscriptionService()