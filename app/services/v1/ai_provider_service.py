from sqlalchemy.orm import Session

from app.db.models.ai_provider import AIProvider


class AIProviderService:

    def get_provider(
        self,
        db: Session,
        provider: str,
        model: str,
    ) -> AIProvider | None:

        return (
            db.query(AIProvider)
            .filter(
                AIProvider.provider == provider,
                AIProvider.model == model,
                AIProvider.is_active.is_(True),
            )
            .order_by(AIProvider.priority.asc())
            .first()
        )

    def get_by_id(
        self,
        db: Session,
        provider_id: int, 
    ) -> AIProvider | None:

        return (
            db.query(AIProvider)
            .filter(AIProvider.id == provider_id)
            .first()
        )

    def get_all(
        self,
        db: Session,
    ):

        return (
            db.query(AIProvider)
            .filter(AIProvider.is_active.is_(True))
            .order_by(AIProvider.priority.asc())
            .all()
        )
    
    def get_default_provider(
        self,
        db: Session,
    ) -> AIProvider | None:

        return (
            db.query(AIProvider)
            .filter(AIProvider.is_active.is_(True))
            .order_by(AIProvider.priority.asc())
            .first()
        )

ai_provider_service = AIProviderService()