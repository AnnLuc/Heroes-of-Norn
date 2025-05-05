# app/schemas/skill.py

from pydantic import BaseModel
from typing import List, Optional

# Модели для навыков
# Этот модуль содержит схемы для работы с навыками.

class SkillBase(BaseModel):
    """
    Базовая модель для навыков.
    Включает название, идентификатор характеристики и бонус для навыка.
    """
    name: str
    attribute_id: int  # Ссылаемся на ID характеристики
    bonus: int = 0  # Бонус для навыка

class SkillCreate(SkillBase):
    """
    Модель для создания нового навыка.
    Наследует все поля от SkillBase.
    """
    pass

class SkillUpdate(SkillBase):
    """
    Модель для обновления навыка.
    Позволяет обновить название и бонус.
    """
    name: Optional[str] = None
    bonus: Optional[int] = None

class Skill(SkillBase):
    """
    Модель для представления навыка.
    Включает ID навыка.
    """
    id: int

    class Config:
        """
        Конфигурация для работы с объектами, используя ORM (объектно-реляционное отображение).
        """
        orm_mode = True

