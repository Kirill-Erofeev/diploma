import os
import httpx
import shutil

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import (
    status,
    APIRouter,
    Depends,
    UploadFile,
    Form,
    Body,
    File
)
from fastapi.responses import JSONResponse, FileResponse

from backend.core.config import settings
from backend.dependencies import get_db, get_current_user
from backend.models.history_model import History
from backend.models.user_model import User
from backend.utils import (
    automatic_speech_recognition,
    speech_synthesis,
    text_generation,
    text_translation,
)

router = APIRouter()

@router.post("/api/audio")
async def post_audio_data(
        current_user: User = Depends(get_current_user),
        # audio: UploadFile = Body(...),
        audio: UploadFile = File(...),
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
    audio_file_path = os.path.join(
        settings.audio_file_directory,
        settings.audio_file_name
    )
    with open(audio_file_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    ru_prompt = automatic_speech_recognition.audio_to_text(
        audio_file_path=audio_file_path
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
    #     audio_file_path=audio_file_path
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
    async with httpx.AsyncClient(verify=settings.ssl_cert_path) as server:
        with open(audio_file_path, "rb") as f:
            file_data = f.read()
        files = {"file": (settings.audio_file_name, file_data, "audio/wav")}
        response = await server.post(
            f"{settings.client_base_url}/audio",
            files=files,
        )
        response.raise_for_status()
        result = response.json()
    return JSONResponse(
        result,
        status_code=response.status_code
    )
# openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
# openssl req -x509 -out localhost.crt -keyout localhost.key -newkey rsa:2048 -nodes -days 365 -sha256 -subj '/CN=localhost' -addext "subjectAltName=IP:127.0.0.1,DNS:localhost"