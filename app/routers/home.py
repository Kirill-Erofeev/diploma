import os
import shutil
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import (
    status,
    APIRouter,
    Depends,
    File,
    UploadFile,
)
from fastapi.responses import HTMLResponse, JSONResponse

from app.core.config import settings
from app.dependencies import get_db, get_current_user
from app.models.history_model import History
from app.models.user_model import User
from app.utils import speech_to_text, text_generation, text_to_speech, translation

router = APIRouter()

@router.get("/home")
async def get_home_page() -> HTMLResponse:
    file_path = os.path.join(settings.templates_folder, "index.html")
    with open(file_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())

@router.post("/record-audio")
async def post_audio_data(
        current_user: User = Depends(get_current_user),
        audio: UploadFile = File(...),
        db: Session = Depends(get_db)
) -> JSONResponse:
    audio_file_path = "./app/static/audio.wav"
    with open(audio_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    ru_prompt = speech_to_text.audio_to_text(
        file_path=audio_file_path
    )
    en_prompt = translation.translate_text(
        target_language="en",
        text=ru_prompt
    )
    generated_en_text = text_generation.answer_the_question(
        prompt=en_prompt
    )
    generated_ru_text = translation.translate_text(
        target_language="ru",
        text=generated_en_text
    )
    current_datetime = datetime.now().replace(microsecond=0)
    new_record = History(
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