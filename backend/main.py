import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.db import database
from backend.routers import auth, history, home
from backend.core.config import settings
from backend.models import history_model, user_model

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

if __name__ == "__main__":
    # uvicorn backend.main:app --host=127.0.0.1 --port=8001 --ssl-keyfile=./certs/key.pem --ssl-certfile=./certs/cert.pem --reload
    uvicorn.run(
        app,
        host="127.0.0.1",
        # host="0.0.0.0",
        port=8001,
        ssl_keyfile=settings.ssl_key_path,
        ssl_certfile=settings.ssl_cert_path
    )