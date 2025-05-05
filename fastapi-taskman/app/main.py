# app/main.py
"""Основной модуль для настройки и запуска приложения FastAPI."""

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.routes import users, campaigns, characters, character_roles, auth
from app.models.database import init_db


# Определяем lifespan функцию
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan функция для инициализации базы данных при старте приложения.
    """
    init_db()  # создаёт таблицы
    yield


# Инициализация приложения FastAPI
app = FastAPI(
    lifespan=lifespan,
    title="D&D Character and Campaign Manager",
    description=(
        "REST-сервис для управления персонажами и игровыми кампаниями по типу D&D. "
        "Позволяет игрокам создавать и управлять своими персонажами, "
        "а мастерам просматривать всех участников своей кампании. "
        "Поддерживается разграничение доступа, авторизация и гибкая структура для будущих расширений, "
        "включая автоматические расчёты бросков кубиков и боевых характеристик."
    ),
    version="0.1.0",
    contact={
        "name": "Проект D&D Manager",
        "url": "https://github.com/ваш-профиль/dnd-manager",  # заменить на реальный URL
        "email": "ваш.email@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    }
)


# Подключение статики и шаблонов
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Основные маршруты
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Главная страница, отображаемая пользователю.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    """
    Страница регистрации пользователя.
    """
    return templates.TemplateResponse("auth/register.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """
    Страница входа пользователя.
    """
    return templates.TemplateResponse("auth/login.html", {"request": request})


# Подключение всех маршрутов
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(characters.router)
app.include_router(character_roles.router)
app.include_router(auth.router)

