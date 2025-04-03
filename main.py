import shutil
from datetime import datetime
from sqlalchemy.orm import Session
from text_to_speech import audio_to_text
from fastapi import FastAPI, File, UploadFile, Depends, status, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from datetime import datetime
import models, schemas, auth
from fastapi.security import OAuth2PasswordBearer
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

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

@app.get("/login")
async def root():
    return FileResponse("public/login.html")

@app.post("/login")
async def postdata(username = Form(), password = Form(), db: Session = Depends(get_db)):
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
async def register_user(
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

@app.get("/")
async def root():
    return FileResponse("public/index.html")

@app.get("/api")
async def main2():
    return FileResponse("public/history.html")

@app.post("/hello")
async def hello(
        current_user: models.User = Depends(get_current_user),
        audio: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    audio_file_path = "audio.wav"
    with open(audio_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    transcribed_text = audio_to_text(audio_file_path)
    # print("text", transcribed_text)
    current_datetime = datetime.now().replace(microsecond=0)
    new_record = models.History(
        date_time=current_datetime,
        request=transcribed_text,
        response="Hello",
        username=current_user.username
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"message": "Файл успешно загружен", "filename": audio.filename}

@app.get("/api/history")
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

@app.get("/api/history/{information}")
async def get_person(
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