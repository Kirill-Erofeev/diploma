import os

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.dependencies import get_db, get_current_user
from app.models.history_model import History
from app.models.user_model import User

router = APIRouter()

@router.get("/history")
async def get_history_page() -> HTMLResponse:
    file_path = os.path.join(settings.templates_folder, "history.html")
    with open(file_path, encoding="utf-8") as f:
        return HTMLResponse(f.read())

@router.get("/get-history")
async def get_history(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):#-> models.History:
    history = db.query(History).filter(
        History.username == current_user.username
    ).all()
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация не найдена"
        )
    return history

@router.get("/get-history/{information}")
async def get_selected_history(
        information: str,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
):# -> models.History:
    selected_history = db.query(History).filter(
        History.username.is_(current_user.username) &
        (History.id.is_(information) |
        History.request.contains(information) |
        History.response.contains(information))
    ).all()
    if not selected_history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Информация не найдена"
        )
    return selected_history