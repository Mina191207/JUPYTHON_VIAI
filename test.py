from app.services.v1.vnpay_service import create_payment_url
from app.db.database import SessionLocal
from app.db.models.payment import Payment

db = SessionLocal()

payment = db.query(Payment).filter(Payment.id == 1).first()

url = create_payment_url(payment, "127.0.0.1")

print(url)