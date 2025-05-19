import os

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

from frontend.core.config import settings

router = APIRouter()

@router.get("/")
def redirect_to_auth():
    return RedirectResponse("/auth")

@router.get("/auth", response_class=HTMLResponse)
async def get_authorization_page() -> HTMLResponse:
    file_path = os.path.join(settings.templates_folder, "auth.html")
    with open(file_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())