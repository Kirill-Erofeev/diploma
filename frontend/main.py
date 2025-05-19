import os
import uvicorn

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import auth, history, home
from app.core.config import settings

app = FastAPI()
app.include_router(history.router)
app.include_router(home.router)
app.include_router(auth.router)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join("frontend", "static")),
    name="static"
)

if __name__ == "__main__":
    # uvicorn frontend.main:app --host=127.0.0.1 --port=8000 --ssl-keyfile=./certs/key.pem --ssl-certfile=./certs/cert.pem --reload
    uvicorn.run(
        app,
        host="127.0.0.1",
        # host="0.0.0.0",
        port=8000,
        ssl_keyfile=settings.ssl_key_path,
        ssl_certfile=settings.ssl_cert_path
    )