# app/routes/users.py
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.user import UserCreate
from app.crud import crud_user
from app.auth.hash import hash_password
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/register", response_class=HTMLResponse)
async def register_post(
    request: Request,
    nickname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя."""
    user_data = UserCreate(nickname=nickname, email=email, password=password)

    existing_user = crud_user.get_user_by_email(db, user_data.email)
    if existing_user:
        return templates.TemplateResponse("auth/register.html", {"request": request, "message": "Почта уже занята"})

    hashed_password = hash_password(user_data.password)
    crud_user.create_user(db, user_data, hashed_password)

    return templates.TemplateResponse("auth/register.html", {"request": request, "message": "Вы зарегистрированы! Теперь войдите в систему"})


@router.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    """Шаблон страницы регистрации."""
    return templates.TemplateResponse("auth/register.html", {"request": request})
