import aiofiles
import asyncio
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
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
        content = await f.read()
    return HTMLResponse(content)

@router.post("/audio")
async def play_audio(file: UploadFile = File(...)):
    file_path = os.path.join("./backend/static/", file.filename)
    async with aiofiles.open(file_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)
    system = platform.system()
    try:
        if system == "Windows":
            await asyncio.to_thread(os.system, f"start {file_path}")
            # os.system(f"start {file_path}")
            # os.startfile(file_path)
        elif system == "Linux":
            await asyncio.create_subprocess_exec("xdg-open", file_path)
            # subprocess.Popen(["xdg-open", file_path])
            # await asyncio.create_subprocess_exec("aplay", file_path)
            # subprocess.Popen(["aplay", file_path])
            # subprocess.run(["ffplay", "-nodisp", "-autoexit", file_path], check=True)
    except Exception as e:
        return JSONResponse(
            f"Ошибка воспроизведения",
            status_code=status.HTTP_502_BAD_GATEWAY
        )
    return JSONResponse(
        f"Аудио воспроизведено",
        status_code=status.HTTP_200_OK
    )