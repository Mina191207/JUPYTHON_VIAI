from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.models.credit_transaction import CreditTransaction


class CreditService:

    def _get_user(self, db: Session, user_id: int):

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return user

    def get_balance(self, db: Session, user_id: int):

        user = self._get_user(db, user_id)

        return {
            "credit_balance": user.credit_balance
        }

    def add_credit(
        self,
        db: Session,
        user_id: int,
        amount: int,
        reason: str,
    ):

        if amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )

        user = self._get_user(db, user_id)

        after = user.credit_balance + amount

        user.credit_balance = after

        transaction = CreditTransaction(
            user_id=user.id,
            type="ADD",
            amount=amount,
            balance_after=after,
            description=reason,
        )

        db.add(transaction)

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(user)
        db.refresh(transaction)

        return {
            "message": "Add credit successfully",
            "balance": user.credit_balance,
            "transaction": transaction.id
        }

    def deduct_credit(
        self,
        db: Session,
        user_id: int,
        amount: int,
        reason: str,
    ):

        if amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Amount must be greater than 0"
            )

        user = self._get_user(db, user_id)

        if user.credit_balance < amount:
            raise HTTPException(
                status_code=400,
                detail="Not enough credit"
            )

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

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        db.refresh(user)
        db.refresh(transaction)

        return {
            "message": "Deduct credit successfully",
            "balance": user.credit_balance,
            "transaction": transaction.id
        }

    def get_history(
        self,
        db: Session,
        user_id: int,
    ):

        self._get_user(db, user_id)

        transactions = (
            db.query(CreditTransaction)
            .filter(CreditTransaction.user_id == user_id)
            .order_by(CreditTransaction.created_at.desc())
            .all()
        )

        return transactions


credit_service = CreditService()