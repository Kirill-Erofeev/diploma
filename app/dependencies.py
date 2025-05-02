from sqlalchemy.orm import Session
from fastapi import (
    status,
    Depends,
    HTTPException,
)

from app.db.database import SessionLocal
from app.models.user_model import User
from app.core import security

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
        token: str = Depends(security.oauth2_scheme),
        db: Session = Depends(get_db)
) -> User | None:
    username = security.verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Ошибка авторизации",
        )
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user