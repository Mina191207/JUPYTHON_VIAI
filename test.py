from app.db.database import SessionLocal
from app.db.models.user import User

db = SessionLocal()

users = db.query(User).all()

for u in users:
    print(u.id, u.email, u.password_hash)

db.close()