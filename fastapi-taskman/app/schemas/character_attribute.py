# app/schemas/character_attribute.py

from pydantic import BaseModel
from typing import Optional

# Модели для атрибутов персонажей в рамках кампании.
# Этот модуль содержит схемы для работы с аттрибутами персонажей.

class CharacterAttributeBase(BaseModel):
    """
    Базовая модель для атрибута персонажа.
    Включает ID персонажа, ID атрибута и значение атрибута для конкретного персонажа.
    """
    character_id: int
    attribute_id: int
    value: int  # Значение атрибута для конкретного персонажа

class CharacterAttributeCreate(CharacterAttributeBase):
    """
    Модель для создания атрибута персонажа.
    Наследует все поля от CharacterAttributeBase.
    """
    pass

class CharacterAttributeUpdate(CharacterAttributeBase):
    """
    Модель для обновления атрибута персонажа.
    Позволяет обновить только значение атрибута.
    """
    value: Optional[int] = None

class CharacterAttribute(CharacterAttributeBase):
    """
    Модель для представления атрибута персонажа с ID.
    """
    id: int

    class Config:
        """
        Конфигурация для работы с объектами, используя ORM.
        """
        orm_mode = True

