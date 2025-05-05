# app/crud/crud_user.py

"""
Модуль для работы с пользователями в базе данных.
Предоставляет функции для получения пользователя по email и создания нового пользователя.
"""

from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.user import UserCreate

def get_user_by_email(db: Session, email: str):
    """
    Получает пользователя из базы данных по email.

    Аргументы:
    db (Session): объект сессии для взаимодействия с базой данных.
    email (str): email пользователя.

    Возвращает:
    User: пользователь с указанным email, если он существует, иначе None.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate, hashed_password: str):  
    """
    Создаёт нового пользователя в базе данных.

    Аргументы:
    db (Session): объект сессии для взаимодействия с базой данных.
    user (UserCreate): данные для создания нового пользователя.
    hashed_password (str): зашифрованный пароль.

    Возвращает:
    User: созданный пользователь.
    """
    db_user = User(
        nickname=user.nickname,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
