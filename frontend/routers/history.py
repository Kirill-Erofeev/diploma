import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from frontend.core.config import settings

router = APIRouter()

@router.get("/history", response_class=HTMLResponse)
async def get_history_page() -> HTMLResponse:
    file_path = os.path.join(settings.templates_directory, "history.html")
    with open(file_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())