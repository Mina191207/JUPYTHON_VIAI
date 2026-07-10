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
        .filter(User.username == form_data.username)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    if not verify_password(
        form_data.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "sub": db_user.username,
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
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role,
    }

@auth.post("/logout")
def logout(
    current_user: User = Depends(get_current_user)
):
    logger.info(f"{current_user.username} logout")

    return {
        "message": "Logout success"
    }