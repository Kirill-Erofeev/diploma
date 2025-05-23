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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Access-Token", "Token-Type"],
)

# Запуск сервера осуществляется из командной строки при помощи команды ниже
# uvicorn backend.main:app --host=127.0.0.1 --port=8001 --ssl-keyfile=./certs/localhost.key --ssl-certfile=./certs/localhost.crt --reload