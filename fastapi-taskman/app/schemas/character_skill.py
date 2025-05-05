# app/schemas/character_skill.py

from pydantic import BaseModel
from typing import List, Optional

# Модели для навыков персонажей
# Этот модуль содержит схемы для работы с навыками персонажей.

class CharacterSkillBase(BaseModel):
    """
    Базовая модель для навыков персонажа.
    Включает идентификаторы персонажа и навыка, а также бонус для конкретного персонажа.
    """
    character_id: int
    skill_id: int
    bonus: int  # Бонус для конкретного персонажа

class CharacterSkillCreate(CharacterSkillBase):
    """
    Модель для создания навыка персонажа.
    Наследует от CharacterSkillBase без изменений.
    """
    pass

class CharacterSkillUpdate(CharacterSkillBase):
    """
    Модель для обновления навыка персонажа.
    Позволяет обновить бонус, делая его необязательным.
    """
    bonus: Optional[int] = None

class CharacterSkill(CharacterSkillBase):
    """
    Модель для представления навыка персонажа.
    Включает идентификатор навыка.
    """
    id: int

    class Config:
        """
        Конфигурация для работы с объектами, используя ORM (объектно-реляционное отображение).
        """
        orm_mode = True

