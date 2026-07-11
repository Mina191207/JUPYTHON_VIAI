from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models.user import User
from app.utils.dependencies import oauth2_scheme
from app.utils.jwt import decode_access_token


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    email: str= payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    db_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return db_user