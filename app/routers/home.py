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
    Form,
    Body
)
from fastapi.responses import HTMLResponse, JSONResponse

from app.core.config import settings
from app.dependencies import get_db, get_current_user
from app.models.history_model import History
from app.models.user_model import User
from app.utils import (
    automatic_speech_recognition,
    speech_synthesis,
    text_generation,
    text_translation,
)

router = APIRouter()

@router.get("/home")
async def get_home_page() -> HTMLResponse:
    file_path = os.path.join(settings.templates_folder, "index.html")
    with open(file_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())

@router.post("/api/audio")
async def post_audio_data(
        current_user: User = Depends(get_current_user),
        audio: UploadFile = Body(...),
        max_sentences: int = Form(...),
        db: Session = Depends(get_db)
) -> JSONResponse:
    voices = [
        # "Anna",
        "Artemiy",
        # "Elena",
        "Evgeniy-Rus",
        "Mikhail",
        "Pavel",
        "Seva",
        "Timofey",
        "Vitaliy",
        "Vitaliy-ng",
        "Yuriy",
    ]
    # audio_file_path = "./app/static/audio.wav"
    with open(settings.audio_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    ru_prompt = automatic_speech_recognition.audio_to_text(
        audio_file_path=settings.audio_file_path
    )
    en_prompt = text_translation.translate_text(
        target_language="en",
        text=ru_prompt
    )
    generated_en_text = text_generation.answer_the_question(
        prompt=en_prompt,
        max_sentences=max_sentences
    )
    generated_ru_text = text_translation.translate_text(
        target_language="ru",
        text=generated_en_text
    )
    # speech_synthesis.text_to_speech_6(
    #     text=generated_ru_text,
    #     voice="Vitaliy-ng",
    #     audio_file_path=settings.audio_file_path
    # )
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