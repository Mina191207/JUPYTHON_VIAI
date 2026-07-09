from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models.user import User
from app.db.models.credit_transaction import CreditTransaction


class CreditService:

    def get_balance(self, db: Session, user_id: int):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(404, "User not found")

        return user.credit_balance

    def add_credit(
        self,
        db: Session,
        user_id: int,
        amount: int,
        reason: str,
    ):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(404, "User not found")

        before = user.credit_balance
        after = before + amount

        user.credit_balance = after

        transaction = CreditTransaction(
            user_id=user.id,
            type="ADD",
            amount=amount,
            balance_after=after,
            description=reason,
        )

        db.add(transaction)

        db.commit()

        db.refresh(user)

        return after

    def deduct_credit(
        self,
        db: Session,
        user_id: int,
        amount: int,
        reason: str,
    ):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(404, "User not found")

        if user.credit_balance < amount:
            raise HTTPException(400, "Not enough credit")

        after = user.credit_balance - amount

        user.credit_balance = after

        transaction = CreditTransaction(
            user_id=user.id,
            type="DEDUCT",
            amount=-amount,
            balance_after=after,
            description=reason,
        )

        db.add(transaction)

        db.commit()

        db.refresh(user)

        return after


credit_service = CreditService()