from fastapi import APIRouter

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.db.models.user import User
from app.utils.security import verify_password
from app.utils.jwt import create_access_token
from app.services.v1.auth_service import get_current_user

from fastapi import HTTPException

from loguru import logger

from app.schemas.auth import RegisterRequest
from app.utils.security import hash_password


auth = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@auth.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": db_user.email,
            "id": db_user.id,
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@auth.get("/me")
def me(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "picture": current_user.picture,
        "phone_number": current_user.phone_number,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role,
    }

@auth.post("/logout")
def logout(
    current_user: User = Depends(get_current_user)
):
    logger.info(f"{current_user.email} logout")

    return {
        "message": "Logout success"
    }

@auth.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    # Kiểm tra email đã tồn tại
    email_exists = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Kiểm tra email đã tồn tại
    email_exists = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if email_exists:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Tạo user mới
    new_user = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        phone_number=request.phone_number,
        password_hash=hash_password(request.password),
        role="user",
        credit_balance=0,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Register successfully",
        "id": new_user.id,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
    }