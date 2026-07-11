from sqlalchemy.orm import Session

from app.db.models.plan import Plan


class PlanService:

    def get_all(self, db: Session):

        return (
            db.query(Plan)
            .filter(Plan.is_active == True)
            .order_by(Plan.price)
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        plan_id: int,
    ):

        return (
            db.query(Plan)
            .filter(
                Plan.id == plan_id,
                Plan.is_active == True,
            )
            .first()
        )


plan_service = PlanService()