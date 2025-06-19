import aiofiles
import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from frontend.core.config import settings

router = APIRouter()

@router.get("/history", response_class=HTMLResponse)
async def get_history_page() -> HTMLResponse:
    file_path = os.path.join(settings.templates_directory, "history.html")
    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
        content = await f.read()
    return HTMLResponse(content)