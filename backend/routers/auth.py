from sqlalchemy.orm import Session
from fastapi import (
    status,
    APIRouter,
    Depends,
    Form,
    HTTPException,
)
from fastapi.responses import JSONResponse

from backend.core import security
from backend.dependencies import get_db
from backend.models.user_model import User
from backend.schemas import token

router = APIRouter()

@router.post("/api/auth/login", response_model=token.Token)
async def post_authorization_data(
        username = Form(),
        password = Form(),
        db: Session = Depends(get_db)
) -> JSONResponse:
    user = db.query(User).filter(User.username == username).first()
    if not user or not security.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Неверное имя пользователя или пароль"
        )
    access_token = security.create_access_token(data={"sub": user.username})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={"Access-Token": access_token, "Token-Type": "Bearer"},
        content="Вход выполнен"
    )

@router.post("/api/auth/register")
async def post_register_data(
        username = Form(),
        password = Form(),
        db: Session = Depends(get_db)
) -> JSONResponse:
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с данным именем уже существует"
        )
    hashed_password = security.get_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Пользователь успешно зарегистрирован"
    )