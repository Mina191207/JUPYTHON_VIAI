from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.v1.ai_provider_service import ai_provider_service

router = APIRouter(prefix="/ai-provider", tags=["AI Provider"])


@router.get("/test")
def test_provider(db: Session = Depends(get_db)):
    provider = ai_provider_service.get_provider(
        db=db,
        provider="OpenAI",
        model="gpt-4o",
    )

    if provider is None:
        return {"message": "Provider not found"}

    return {
        "id": provider.id,
        "provider": provider.provider,
        "model": provider.model,
        "base_url": provider.base_url,
        "priority": provider.priority,
    }