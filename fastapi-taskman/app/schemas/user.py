# app/schemas/user.py

from pydantic import BaseModel, EmailStr

# Модели для работы с пользователями.
# Этот модуль содержит схемы для регистрации пользователей, вывода информации о пользователях и их создания.

class UserBase(BaseModel):
    """
    Базовая модель для пользователя.
    Включает обязательные поля email и nickname для пользователя.
    """
    email: EmailStr
    nickname: str

class UserCreate(BaseModel):
    """
    Модель для создания пользователя.
    Включает обязательные поля email, nickname и password.
    """
    nickname: str  # это обязательное поле
    email: str
    password: str

    class Config:
        """
        Конфигурация для работы с аттрибутами модели в Pydantic V2.
        """
        from_attributes = True  # или from_attributes для Pydantic V2

class UserOut(UserBase):
    """
    Модель для вывода информации о пользователе.
    Включает поля email, nickname и id.
    """
    id: int

    class Config:
        """
        Конфигурация для работы с аттрибутами модели в Pydantic V2.
        """
        from_attributes = True

