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
        prompt_tokens: int,
        completion_tokens: int,
        total_tokens: int,
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
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
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
        providers = ai_provider_service.get_all_active(db)
        subscription = data["subscription"]

        script = None
        provider = None

        for p in providers:

            try:

                result = llm_service.generate_script(
                    provider_name=p.provider,
                    model_name=p.model,
                    api_key=p.api_key,
                    base_url=p.base_url,
                    video_subject=video_subject,
                    language=language,
                    paragraph_number=paragraph_number,
                )

                script = result["script"]
                provider = p
                break

            except Exception as e:

                print(f"{p.provider} failed:", e)

        if provider is None:
            raise HTTPException(
                status_code=500,
                detail="No AI provider available",
            )

        self._finish_ai_request(
            db=db,
            user=user,
            provider=provider,
            subscription=subscription,
            required_credit=required_credit,
            reason="Generate video script",
            prompt_tokens=result["prompt_tokens"],
            completion_tokens=result["completion_tokens"],
            total_tokens=result["total_tokens"],
        )

        return {
            "script": script,
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "total_tokens": result["total_tokens"],
        }
    
    def estimate(
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

        subscription = data["subscription"]

        estimated_prompt_tokens = 300
        estimated_completion_tokens = paragraph_number * 500
        estimated_total_tokens = (
            estimated_prompt_tokens
            + estimated_completion_tokens
        )

        return {
            "estimated_prompt_tokens": estimated_prompt_tokens,
            "estimated_completion_tokens": estimated_completion_tokens,
            "estimated_total_tokens": estimated_total_tokens,
            "estimated_credit": 0 if subscription else required_credit,
            "has_subscription": subscription is not None,
        }
    
    def generate_terms(
        self,
        db: Session,
        user_id: int,
        video_subject: str,
        video_script: str,
        amount: int,
        match_script_order: bool = False,
    ):

        required_credit = 5

        data = self._prepare_ai_request(
            db=db,
            user_id=user_id,
            required_credit=required_credit,
        )

        user = data["user"]
        subscription = data["subscription"]

        providers = ai_provider_service.get_all_active(db)

        provider = None
        result = None

        for p in providers:

            try:

                result = llm_service.generate_terms(
                    provider_name=p.provider,
                    model_name=p.model,
                    api_key=p.api_key,
                    base_url=p.base_url,
                    video_subject=video_subject,
                    video_script=video_script,
                    amount=amount,
                    match_script_order=match_script_order,
                )
                if result:
                    provider = p
                    break

            except Exception as e:

                print(f"{p.provider} failed:", e)

        if provider is None:
            raise HTTPException(
                status_code=500,
                detail="No AI provider available",
            )

        self._finish_ai_request(
            db=db,
            user=user,
            provider=provider,
            subscription=subscription,
            required_credit=required_credit,
            reason="Generate search terms",
            prompt_tokens=result["prompt_tokens"],
            completion_tokens=result["completion_tokens"],
            total_tokens=result["total_tokens"],
        )

        return result
    
    def generate_social_metadata(
        self,
        db: Session,
        user_id: int,
        video_subject: str,
        video_script: str,
    ):
        required_credit = 5

        data = self._prepare_ai_request(
            db=db,
            user_id=user_id,
            required_credit=required_credit,
        )

        user = data["user"]
        subscription = data["subscription"]

        providers = ai_provider_service.get_all_active(db)

        provider = None
        result = None

        for p in providers:
            try:
                result = llm_service.generate_social_metadata(
                    provider_name=p.provider,
                    model_name=p.model,
                    api_key=p.api_key,
                    base_url=p.base_url,
                    video_subject=video_subject,
                    video_script=video_script,
                )

                if result:
                    provider = p
                    break

            except Exception as e:
                print(f"{p.provider} failed:", e)

        if provider is None:
            raise HTTPException(
                status_code=500,
                detail="No AI provider available",
            )

        self._finish_ai_request(
            db=db,
            user=user,
            provider=provider,
            subscription=subscription,
            required_credit=required_credit,
            reason="Generate social metadata",
            prompt_tokens=result["prompt_tokens"],
            completion_tokens=result["completion_tokens"],
            total_tokens=result["total_tokens"],
        )

        return result

ai_service = AIService()