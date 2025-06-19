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

# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout unified_key.key -out unified_cert.crt -config san.cnf -extensions v3_req
# Запуск сервера осуществляется из командной строки при помощи команды ниже
# uvicorn frontend.main:app --host=0.0.0.0 --port=8000 --ssl-keyfile=./certs/unified_key.key --ssl-certfile=./certs/unified_cert.crt --reload