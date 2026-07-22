from app.services.v1.ai_provider_service import ai_provider_service
from app.services.v1.vnpay_service import create_payment_url
from app.db.database import SessionLocal
from app.db.models.payment import Payment

db = SessionLocal()
providers = ai_provider_service.get_all_active(db)

for p in providers:
    print(p.provider, p.priority)   