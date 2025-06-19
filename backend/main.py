import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
from starlette.concurrency import run_in_threadpool
from transformers import AutoModelForCausalLM, AutoTokenizer, MarianMTModel, MarianTokenizer

from backend.db import database
from backend.core import model_registry
from backend.core.config import settings
from backend.models import history_model, user_model
from backend.routers import auth, history, home

STATIC_DIRECTORY = os.path.join(settings.audio_file_directory)
os.makedirs(STATIC_DIRECTORY, exist_ok=True)

history_model.Base.metadata.create_all(bind=database.engine)
user_model.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(history.router)
app.include_router(home.router)
app.include_router(auth.router)

@app.on_event("startup")
async def load_models():
    model_path = os.path.join(settings.lm_directory, "Whisper")
    model_registry.whisper_model = await run_in_threadpool(
        WhisperModel, model_path, compute_type="int8", device="cpu"
    )

    model_path = os.path.join(settings.lm_directory, "Helsinki-ru-en")
    model_registry.ru_en_tokenizer = await run_in_threadpool(
        MarianTokenizer.from_pretrained, "Helsinki-NLP/opus-mt-ru-en"
        # MarianTokenizer.from_pretrained, model_path
    )
    model_registry.ru_en_model = await run_in_threadpool(
        MarianMTModel.from_pretrained, "Helsinki-NLP/opus-mt-ru-en"
        # MarianMTModel.from_pretrained, model_path
    )

    model_path = os.path.join(settings.lm_directory, "Helsinki-en-ru")
    model_registry.en_ru_tokenizer = await run_in_threadpool(
        MarianTokenizer.from_pretrained, "Helsinki-NLP/opus-mt-en-ru"
        # MarianTokenizer.from_pretrained, model_path
    )
    model_registry.en_ru_model = await run_in_threadpool(
        MarianMTModel.from_pretrained, "Helsinki-NLP/opus-mt-en-ru"
        # MarianMTModel.from_pretrained, model_path
    )

    model_path = os.path.join(settings.lm_directory, "SmallDoge")
    model_registry.small_doge_tokenizer = await run_in_threadpool(
        AutoTokenizer.from_pretrained, model_path
    )
    model_registry.small_doge_model = await run_in_threadpool(
        AutoModelForCausalLM.from_pretrained, model_path, trust_remote_code=True
    )

origins = [
    "http://127.0.0.1:8000",
    "https://127.0.0.1:8000",
    "http://localhost:8000",
    "https://localhost:8000",
    "http://0.0.0.0:8000",
    "https://0.0.0.0:8000",
    "http://10.4.35.51:8000",
    "https://10.4.35.51:8000",
    "http://10.4.35.13:8000",
    "https://10.4.35.13:8000",
    "http://192.168.1.14:8000",
    "https://192.168.1.14:8000",
    "http://192.168.10.154:8000",
    "https://192.168.10.154:8000",
    "http://192.168.10.230:8000",
    "https://192.168.10.230:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Token", "Token-Type"],
)

# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout unified_key.key -out unified_cert.crt -config san.cnf -extensions v3_req
# Запуск сервера осуществляется из командной строки при помощи команды ниже
# uvicorn backend.main:app --host=0.0.0.0 --port=8001 --ssl-keyfile=./certs/unified_key.key --ssl-certfile=./certs/unified_cert.crt --reload