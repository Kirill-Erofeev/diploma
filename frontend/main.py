import json
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from frontend.routers import auth, history, home
from frontend.core.config import settings

STATIC_DIRECTORY = os.path.join("frontend", "static")
CONFIG_FILE = os.path.join(STATIC_DIRECTORY, "config.json")
os.makedirs(STATIC_DIRECTORY, exist_ok=True)

with open(CONFIG_FILE, "w") as f:
    json.dump({"SERVER_BASE_URL": settings.server_base_url}, f)

app = FastAPI()
app.include_router(history.router)
app.include_router(home.router)
app.include_router(auth.router)
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIRECTORY),
    name="static"
)

# Запуск сервера осуществляется из командной строки при помощи команды ниже
# uvicorn frontend.main:app --host=127.0.0.1 --port=8000 --ssl-keyfile=./certs/localhost.key --ssl-certfile=./certs/localhost.crt --reload