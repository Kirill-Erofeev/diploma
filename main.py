import shutil
from datetime import datetime
from sqlalchemy.orm import Session
from speech_to_text import audio_to_text
from fastapi import FastAPI, File, UploadFile, Depends, status, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime
import models, schemas, auth
from fastapi.security import OAuth2PasswordBearer
from database import engine, get_db
from text_generation import answer_the_question
from translation import translate_text

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/")

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
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
async def get_authorization_page():
    return FileResponse("public/authorization.html")

@app.post("/")
async def post_authorization_data(
        username = Form(),
        password = Form(),
        db: Session = Depends(get_db)
):
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
        db: Session = Depends(get_db)
):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь с данным именем уже существует"
        )
    hashed_password = auth.get_password_hash(password)
    new_user = models.User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Пользователь успешно зарегистрирован"
    )

@app.get("/home")
async def get_home_page():
    return FileResponse("public/index.html")

@app.post("/record-audio")
async def post_audio_data(
        current_user: models.User = Depends(get_current_user),
        audio: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    audio_file_path = "audio.wav"
    with open(audio_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    ru_prompt = audio_to_text(audio_file_path)
    en_prompt = translate_text(target_language="en", text=ru_prompt)
    generated_en_text = answer_the_question(prompt=en_prompt)
    generated_ru_text = translate_text(target_language="ru", text=generated_en_text)
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
async def get_history_page():
    return FileResponse("public/history.html")

@app.get("/get-history")
async def get_history(
        current_user: models.User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
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
        db: Session = Depends(get_db),
):
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