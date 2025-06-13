import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import database
from backend.routers import auth, history, home
from backend.core.config import settings
from backend.models import history_model, user_model

STATIC_DIRECTORY = os.path.join(settings.audio_file_directory)
os.makedirs(STATIC_DIRECTORY, exist_ok=True)

history_model.Base.metadata.create_all(bind=database.engine)
user_model.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(history.router)
app.include_router(home.router)
app.include_router(auth.router)

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://127.0.0.1:8000",
    "https://localhost:8000",
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

# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout unified_key.pem -out unified_cert.pem -config san.cnf -extensions v3_req
# Запуск сервера осуществляется из командной строки при помощи команды ниже
# uvicorn backend.main:app --host=0.0.0.0 --port=8001 --ssl-keyfile=./certs/unified_key.pem --ssl-certfile=./certs/unified_cert.pem --reload