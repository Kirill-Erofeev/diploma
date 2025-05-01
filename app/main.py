import os
import shutil
import uvicorn

from dotenv import load_dotenv
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import (
    FastAPI,
    File,
    UploadFile,
    Depends,
    status,
    Form,
    HTTPException
)
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer

from app import (
    auth,
    schemas,
    speech_to_text,
    text_generation,
    text_to_speech,
    translation,
)
from app.database import db, models

load_dotenv()
SSL_KEY_PATH = os.getenv("SSL_KEY_PATH")
SSL_CERT_PATH = os.getenv("SSL_CERT_PATH")
LM_FOLDER = os.getenv("LM_FOLDER")
models.Base.metadata.create_all(bind=db.engine)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(db.get_db)
) -> models.User | None:
    username = auth.verify_token(token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Ошибка авторизации",
        )
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user

@app.get("/")
async def get_authorization_page() -> FileResponse:
    return FileResponse("app/templates/authorization.html")

@app.post("/", response_model=schemas.Token)
async def post_authorization_data(
        username = Form(),
        password = Form(),
        db: Session = Depends(db.get_db)
) -> JSONResponse:
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"},
            detail="Неверное имя пользователя или пароль"
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        headers={"Access-Token": access_token, "Token-Type": "Bearer"},
        content="Вход выполнен"
    )

@app.post("/register")
async def post_register_data(
        username = Form(),
        password = Form(),
        db: Session = Depends(db.get_db)
) -> JSONResponse:
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с данным именем уже существует"
        )
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content="Пользователь успешно зарегистрирован"
    )

@app.get("/home")
async def get_home_page() -> FileResponse:
    return FileResponse("app/templates/index.html")

@app.post("/record-audio")
async def post_audio_data(
        current_user: models.User = Depends(get_current_user),
        audio: UploadFile = File(...),
        db: Session = Depends(db.get_db)
) -> JSONResponse:
    audio_file_path = "./app/static/audio.wav"
    with open(audio_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    ru_prompt = speech_to_text.audio_to_text(
        audio_file_path,
        LM_FOLDER=LM_FOLDER
    )
    en_prompt = translation.translate_text(
        target_language="en",
        text=ru_prompt,
        LM_FOLDER=LM_FOLDER
    )
    generated_en_text = text_generation.answer_the_question(
        prompt=en_prompt,
        LM_FOLDER=LM_FOLDER
    )
    generated_ru_text = translation.translate_text(
        target_language="ru",
        text=generated_en_text,
        LM_FOLDER=LM_FOLDER
    )
    current_datetime = datetime.now().replace(microsecond=0)
    new_record = models.History(
        date_time=current_datetime,
        request=ru_prompt,
        response=generated_ru_text,
        username=current_user.username
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Информация обработана"
    )

@app.get("/history")
async def get_history_page() -> FileResponse:
    return FileResponse("app/templates/history.html")

@app.get("/get-history")
async def get_history(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(db.get_db)
):#-> models.History:
    history = db.query(models.History).filter(
        models.History.username == current_user.username
    ).all()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация не найдена"
        )
    return history

@app.get("/get-history/{information}")
async def get_selected_history(
        information: str,
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(db.get_db),
):# -> models.History:
    selected_history = db.query(models.History).filter(
        models.History.username.is_(current_user.username) &
        (models.History.id.is_(information) |
        models.History.request.contains(information) |
        models.History.response.contains(information))
    ).all()
    if not selected_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация не найдена"
        )
    return selected_history

if __name__ == "__main__":
    uvicorn.run(
        app,
        # host="127.0.0.1",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile=SSL_KEY_PATH,
        ssl_certfile=SSL_CERT_PATH
    )