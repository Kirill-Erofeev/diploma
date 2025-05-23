import os
import platform
import shutil
import subprocess

from fastapi import status, APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse

from frontend.core.config import settings

router = APIRouter()

@router.get("/home", response_class=HTMLResponse)
async def get_home_page() -> HTMLResponse:
    file_path = os.path.join(settings.templates_directory, "index.html")
    with open(file_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())

@router.post("/audio")
def play_audio(file: UploadFile = File(...)):
    file_path = os.path.join("./backend/static/", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    system = platform.system()
    try:
        if system == "Windows":
            os.system(f"start {file_path}")
            # os.startfile(file_path)
        elif system == "Linux":
            try:
                subprocess.run(["aplay", file_path], check=True)
            except subprocess.CalledProcessError:
                subprocess.run(["ffplay", "-nodisp", "-autoexit", file_path], check=True)
    except Exception as e:
        return JSONResponse(
            f"Ошибка воспроизведения",
            status_code=status.HTTP_502_BAD_GATEWAY
        )
    return JSONResponse(
        f"Аудио воспроизведено",
        status_code=status.HTTP_200_OK
    )