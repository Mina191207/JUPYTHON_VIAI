from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.user import User

from app.services.v1.ai_provider_service import ai_provider_service
from app.services.v1.credit_service import credit_service
from app.services.v1.subscription_service import subscription_service
from app.services.v1.usage_service import usage_service
import app.services.v1.llm_service as llm_service

class AIService:
    def _prepare_ai_request(
        self,
        db: Session,
        user_id: int,
        required_credit: int,
    ):
        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found",
            )
        provider = ai_provider_service.get_default_provider(db)

        if provider is None:
            raise HTTPException(
                status_code=404,
                detail="No AI provider available",
            )

        subscription = subscription_service.get_active_subscription(
            db=db,
            user_id=user.id,
        )

        if not subscription:

            enough = credit_service.check_balance(
                db=db,
                user_id=user.id,
                required_credit=required_credit,
            )

            if not enough:
                raise HTTPException(
                    status_code=400,
                    detail="Not enough credit",
                )

        return {
            "user": user,
            "provider": provider,
            "subscription": subscription,
        }
    
    def _finish_ai_request(
        self,
        db: Session,
        user,
        provider,
        subscription,
        required_credit: int,
        reason: str,
    ):
        transaction = None

        if not subscription:
            transaction = credit_service.deduct_credit(
                db=db,
                user_id=user.id,
                amount=required_credit,
                reason=reason,
            )

        usage_service.create(
            db=db,
            user_id=user.id,
            provider_id=provider.id,
            credit_transaction_id=transaction.id if transaction else None,
            model=provider.model,
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            cost=0,
            credit_used=required_credit if not subscription else 0,
        )
        return transaction


    def generate_script(
        self,
        db: Session,
        user_id: int,
        video_subject: str,
        language: str,
        paragraph_number: int,
    ):

        required_credit = 10

        data = self._prepare_ai_request(
            db=db,
            user_id=user_id,
            required_credit=required_credit,
        )

        user = data["user"]
        provider = data["provider"]
        subscription = data["subscription"]
        try:
            script = llm_service.generate_script(
                provider_name=provider.provider,
                model_name=provider.model,
                api_key=provider.api_key,
                base_url=provider.base_url,
                video_subject=video_subject,
                language=language,
                paragraph_number=paragraph_number,
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate script: {str(e)}",
            )

        self._finish_ai_request(
            db=db,
            user=user,
            provider=provider,
            subscription=subscription,
            required_credit=required_credit,
            reason="Generate video script",
        )

        return {
            "script": script,
        }


ai_service = AIService()