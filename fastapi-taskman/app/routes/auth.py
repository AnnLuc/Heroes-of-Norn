# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.models.database import get_db
from app.auth.hash import hash_password, verify_password
from app.crud import crud_user

router = APIRouter(tags=["Auth"])
templates = Jinja2Templates(directory="app/templates")


@router.post("/register", response_model=schemas.user.UserOut)
async def register(
    nickname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """Регистрация нового пользователя."""
    from app.schemas.user import UserCreate

    existing_user = crud_user.get_user_by_email(db, email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(password)
    user_data = UserCreate(nickname=nickname, email=email, password=password)
    user = crud_user.create_user(db, user_data, hashed_pw)
    return user


@router.post("/login")
async def login_post(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Логин пользователя."""
    user = crud_user.get_user_by_email(db, form_data.username)

    # Проверяем, что пользователь существует и что пароли совпадают
    if not user or not verify_password(form_data.password, user.password):
        return templates.TemplateResponse("auth/login.html", {"request": request, "message": "Неверные данные"})
    
    # Если всё совпало
    return templates.TemplateResponse("auth/login.html", {"request": request, "message": "Вход успешен!"})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Шаблон страницы логина."""
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Шаблон страницы регистрации."""
    return templates.TemplateResponse("auth/register.html", {"request": request})
