from app.models.schema import VideoAspect
from app.schemas.schema import VideoParams
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models.user import User
from app.utils import utils

from app.services.v1.video_record_service import video_record_service
from app.services.v1.ai_provider_service import ai_provider_service
from app.services.v1.credit_service import credit_service
from app.services.v1.subscription_service import subscription_service
from app.services.v1.usage_service import usage_service
import app.services.v1.llm_service as llm_service
from app.services.v1 import material_service
from app.services.v1.voice_service import tts
from app.services.v1 import voice_service
from app.services.v1 import video_service

import os
import uuid

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
        charge_credit: bool = True,
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
        if charge_credit:
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
            "provider": provider,
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
        charge_credit: bool = True,
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
        if charge_credit:
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

        return {
            "provider": provider,
            **result,
        }

    def generate_social_metadata(
        self,
        db: Session,
        user_id: int,
        video_subject: str,
        video_script: str,
        charge_credit: bool = True,
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
        if charge_credit:
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
        return {
            "provider": provider,
            **result,
        }
    
    def generate_video(
        self,
        db: Session,
        user_id: int,
        video_subject: str,
        language: str = "",
        paragraph_number: int = 1,
    ):
        required_credit = 20

        data = self._prepare_ai_request(
            db=db,
            user_id=user_id,
            required_credit=required_credit,
        )

        user = data["user"]
        subscription = data["subscription"]

        script = self.generate_script(
            db=db,
            user_id=user_id,
            video_subject=video_subject,
            language=language,
            paragraph_number=paragraph_number,
            charge_credit=False,
        )

        provider = script["provider"]

        terms = self.generate_terms(
            db=db,
            user_id=user_id,
            video_subject=video_subject,
            video_script=script["script"],
            amount=5,
            charge_credit=False,
        )

        metadata = self.generate_social_metadata(
            db=db,
            user_id=user_id,
            video_subject=video_subject,
            video_script=script["script"],
            charge_credit=False,
        )
        audio = self.generate_audio(
            db=db,
            user_id=user_id,
            script=script["script"],
            voice_name="vi-VN-HoaiMyNeural",
            charge_credit=False,
        )
        task_id = str(uuid.uuid4())
        print("Downloading materials...")
        materials = material_service.download_videos(
            task_id=task_id,
            search_terms=terms["terms"],
            source="pexels",
            audio_duration=audio["duration"],
        )

        combined_video_path = os.path.join(
            utils.task_dir(task_id),
            "combined.mp4",
        )
        video_service.combine_videos(
            combined_video_path=combined_video_path,
            video_paths=materials,
            audio_file=audio["audio_path"],
            video_aspect=VideoAspect.portrait,
            max_clip_duration=5,
        )

        params = VideoParams(
            video_subject=video_subject,
            video_script=script["script"],
            video_terms=terms["terms"],
            video_aspect=VideoAspect.portrait,
            voice_name="vi-VN-HoaiMyNeural",
            subtitle_enabled=True,
        )

        final_video_path = os.path.join(
            utils.task_dir(task_id),
            "final.mp4",
        )
        video_service.generate_video(
            video_path=combined_video_path,
            audio_path=audio["audio_path"],
            subtitle_path=audio["subtitle_path"],
            output_file=final_video_path,
            params=params,
        )
        video_record_service.create(
            db=db,
            user_id=user.id,
            task_id=task_id,
            title=metadata["metadata"]["title"],
            file_path=final_video_path,
            credit_used=required_credit,
            duration=int(audio["duration"])
        )
        prompt_tokens = (
            script["prompt_tokens"]
            + terms["prompt_tokens"]
            + metadata["prompt_tokens"]
        )

        completion_tokens = (
            script["completion_tokens"]
            + terms["completion_tokens"]
            + metadata["completion_tokens"]
        )

        total_tokens = (
            script["total_tokens"]
            + terms["total_tokens"]
            + metadata["total_tokens"]
        )
        self._finish_ai_request(
            db=db,
            user=user,
            provider=provider,
            subscription=subscription,
            required_credit=required_credit,
            reason="Generate video",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )

        return {
            "script": script,
            "terms": terms,
            "metadata": metadata,
            "audio": audio,
            "materials": materials,
            "video_path": final_video_path,
        }

    def _generate_audio(self, script: str, voice_name: str, voice_rate: float = 1.0):

        os.makedirs("storage/audio", exist_ok=True)

        filename = f"{uuid.uuid4()}.mp3"

        voice_file = os.path.join(
            "storage",
            "audio",
            filename,
        )

        sub_maker = tts(
            text=script,
            voice_name=voice_name,
            voice_rate=voice_rate,
            voice_file=voice_file,
            voice_volume=1.0,
        )

        if sub_maker is None:
            raise Exception("Generate audio failed")

        subtitle_path = self._save_subtitle(sub_maker)
        print(type(sub_maker))
        print(dir(sub_maker))
        subtitle_path = self._save_subtitle(sub_maker)

        duration = voice_service.get_audio_duration(voice_file)
        return {
            "audio_path": voice_file,
            "subtitle_path": subtitle_path,
            "duration": duration,
        }


    def generate_audio(
        self,
        db: Session,
        user_id: int,
        script: str,
        voice_name: str,
        voice_rate: float = 1.0,
        charge_credit: bool = True,
    ):
        required_credit = 5

        user = None
        subscription = None

        if charge_credit:
            data = self._prepare_ai_request(
                db=db,
                user_id=user_id,
                required_credit=required_credit,
            )

            user = data["user"]
            subscription = data["subscription"]

        providers = ai_provider_service.get_all_active(db)

        if not providers:
            raise HTTPException(
                status_code=500,
                detail="No AI provider available",
            )

        provider = providers[0]

        audio = self._generate_audio(
            script=script,
            voice_name=voice_name,
            voice_rate=voice_rate,
        )

        if charge_credit:
            self._finish_ai_request(
                db=db,
                user=user,
                provider=provider,
                subscription=subscription,
                required_credit=required_credit,
                reason="Generate audio",
                prompt_tokens=0,
                completion_tokens=0,
                total_tokens=0,
            )

        return audio

    def _save_subtitle(
        self,
        sub_maker,
    ):
        os.makedirs("storage/subtitle", exist_ok=True)

        subtitle_path = os.path.join(
            "storage",
            "subtitle",
            f"{uuid.uuid4()}.srt",
        )

        with open(
            subtitle_path,
            "w",
            encoding="utf-8",
        ) as f:
            f.write(sub_maker.get_srt())

        return subtitle_path



ai_service = AIService()