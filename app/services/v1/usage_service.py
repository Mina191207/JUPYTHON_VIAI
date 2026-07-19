from sqlalchemy.orm import Session

from app.db.models.usage_log import UsageLog


class UsageService:

    def create(
        self,
        db: Session,
        user_id: int,
        provider_id: int,
        credit_transaction_id: int | None,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
        cost: float,
        credit_used: int,
    ):

        usage = UsageLog(
            user_id=user_id,
            provider_id=provider_id,
            credit_transaction_id=credit_transaction_id,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost=cost,
            credit_used=credit_used,
        )

        db.add(usage)
        db.commit()
        db.refresh(usage)

        return usage


usage_service = UsageService()