import os

from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from backend.core.config import settings
from backend.dependencies import get_db, get_current_user
from backend.models.history_model import History
from backend.models.user_model import User

router = APIRouter()

@router.get("/api/history")
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

@router.get("/api/history/{information}")
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