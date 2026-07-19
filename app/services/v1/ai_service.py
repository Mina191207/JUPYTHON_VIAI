from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.user import User

from app.services.v1.ai_provider_service import ai_provider_service
from app.services.v1.credit_service import credit_service
from app.services.v1.subscription_service import subscription_service
from app.services.v1.usage_service import usage_service
import app.services.v1.llm_service as llm_service

class AIService:

    def generate_script(
        self,
        db: Session,
        user_id: int,
        video_subject: str,
        language: str,
        paragraph_number: int,
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

        print("=" * 50)
        print("Provider:", provider.provider)
        print("Model:", provider.model)
        print("Base URL:", provider.base_url)
        print("API Key:", provider.api_key[:10] + "...")
        print("=" * 50)

        if provider is None:
            raise HTTPException(
                status_code=404,
                detail="No AI provider available",
            )

        subscription = subscription_service.get_active_subscription(
            db=db,
            user_id=user.id,
        )

        required_credit = 10

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

        script = llm_service.generate_script(
            provider_name=provider.provider,
            model_name=provider.model,
            api_key=provider.api_key,
            base_url=provider.base_url,
            video_subject=video_subject,
            language=language,
            paragraph_number=paragraph_number,
        )

        return {
            "script": script,
        }


ai_service = AIService()