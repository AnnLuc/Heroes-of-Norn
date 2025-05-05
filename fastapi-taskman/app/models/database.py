"""Модуль для работы с базой данных с использованием SQLAlchemy."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import declarative_base

# Пока используем SQLite — локальный файл базы
DATABASE_URL = "sqlite:////home/anna/fastapi-taskman/app/app.db"

# Создаём движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Только для SQLite
)

# Создаём фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    """
    Функция для получения сессии базы данных.

    Используется как зависимость в маршрутах FastAPI для работы с базой данных.
    Открывает сессию, передаёт её в запрос, а затем закрывает после завершения.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Инициализация базы данных.

    Создаёт все таблицы в базе данных.
    """
    from . import models  # Импортируем модели, чтобы они зарегистрировались в Base
    Base.metadata.create_all(bind=engine)

