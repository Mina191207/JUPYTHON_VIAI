from app.db.database import SessionLocal
from app.db.models.user import User
from app.utils.security import verify_password

# Tạo session
db = SessionLocal()

try:
    # Lấy user admin
    db_user = db.query(User).filter(User.username == "admin").first()

    if db_user is None:
        print("Không tìm thấy user admin")
    else:
        print("Password trong DB:", db_user.password_hash)

        result = verify_password(
            "admin123",
            db_user.password_hash
        )

        print("Verify:", result)

finally:
    db.close()

    from app.utils.jwt import create_access_token

token = create_access_token(
    {
        "sub": "admin"
    }
)

print(token)

from app.utils.jwt import decode_access_token

payload = decode_access_token(token)

print("Payload:", payload)
