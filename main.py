import base64
import shutil
from db import db, History, SessionLocal
from datetime import datetime
from sqlalchemy.orm import Session
from text_to_speech import audio_to_text
from requests_toolbelt.multipart import decoder
from fastapi import FastAPI, Body, File, UploadFile, Depends, status
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def root():
    return FileResponse("public/index.html")

@app.get("/api")
def main2():
    return FileResponse("public/history.html")

@app.get("/api/history")
def get_history(db: Session = Depends(get_db)):
    return db.query(History).all()

@app.get("/api/history/{information}")
def get_person(information, db: Session = Depends(get_db)):
    selected_history = db.query(History).filter(
        History.id.is_(information) |
        # History.date_time.contains(information) |
        History.request.contains(information) |
        History.response.contains(information)
    ).all()
    if not selected_history:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Информация не найдена"}
        )
    return selected_history

@app.post("/hello")
#def hello(name = Body(embed=True)):
async def hello(audio: UploadFile = File(...)):
    audio_file_path = "audio.wav"
    with open(audio_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    transcribed_text = audio_to_text(audio_file_path)
    # print("text", transcribed_text)
    current_datetime = datetime.now().replace(microsecond=0)

    new_record = History(
        date_time=current_datetime,
        request=transcribed_text,
        response="Hello"
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    
    return {"message": "Файл успешно загружен", "filename": audio.filename}