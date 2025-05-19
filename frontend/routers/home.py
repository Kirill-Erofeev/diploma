import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.core.config import settings

router = APIRouter()

@router.get("/home", response_class=HTMLResponse)
async def get_home_page() -> HTMLResponse:
    file_path = os.path.join(settings.templates_folder, "index.html")
    with open(file_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())