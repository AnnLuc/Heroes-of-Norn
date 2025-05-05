# app/schemas/character.py

from pydantic import BaseModel
from typing import List, Optional, Dict
from fastapi import Form
from .attribute import Attribute  # Импортируем Attribute
from .skill import Skill  # Импортируем Skill

# Модели для работы с персонажами.
# Этот модуль включает схемы для создания, обновления и вывода информации о персонажах.

class CharacterBase(BaseModel):
    """
    Базовая модель для персонажа.
    Включает имя и описание персонажа.
    """
    name: str
    description: Optional[str] = None

class CharacterCreate(BaseModel):
    """
    Модель для создания персонажа.
    Включает имя, описание, атрибуты и навыки персонажа.
    """
    name: str
    description: Optional[str] = None
    attributes: Dict[int, int] = {}  # ID атрибута: значение
    skills: Dict[int, int] = {}      # ID навыка: бонус

    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        description: Optional[str] = Form(None),
        attributes: Dict[int, int] = Form(...),  # Здесь Form(...) не работает для словаря напрямую
        skills: Dict[int, int] = Form(...),
    ):
        """
        Метод для обработки формы создания персонажа.
        Пытается преобразовать форму в объект, но необходимо обработать атрибуты и навыки вручную.
        """
        # Это невозможно напрямую — решение ниже
        pass

class CharacterUpdate(CharacterBase):
    """
    Модель для обновления информации о персонаже.
    Позволяет обновить имя и описание персонажа.
    """
    name: Optional[str] = None
    description: Optional[str] = None

class Character(CharacterBase):
    """
    Модель персонажа, которая включает атрибуты и навыки.
    Используется для отображения полного персонажа в системе.
    """
    id: int
    campaign_id: Optional[int] = None
    user_id: int
    attributes: List[Attribute]  # Добавляем атрибуты
    skills: List[Skill]  # Добавляем навыки

    class Config:
        """
        Конфигурация для работы с аттрибутами модели в Pydantic V2.
        """
        orm_mode = True

class CharacterOut(BaseModel):
    """
    Модель для вывода информации о персонаже.
    Включает id и имя персонажа.
    """
    id: int
    name: str

