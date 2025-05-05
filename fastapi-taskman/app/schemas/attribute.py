# app/schemas/attribute.py

from pydantic import BaseModel
from typing import Optional

# Модели для характеристик
# Этот модуль содержит схемы для работы с характеристиками персонажей.

class AttributeBase(BaseModel):
    """
    Базовая модель для характеристик.
    Включает название характеристики и тип кубика для её броска.
    """
    name: str
    dice_type: str  # Тип кубика для характеристики (например, 1d4, 1d6 и т.д.)

class AttributeCreate(AttributeBase):
    """
    Модель для создания новой характеристики.
    Наследует все поля от AttributeBase.
    """
    pass

class AttributeUpdate(AttributeBase):
    """
    Модель для обновления характеристики.
    Позволяет обновить название и тип кубика.
    """
    name: Optional[str] = None
    dice_type: Optional[str] = None

class Attribute(AttributeBase):
    """
    Модель для представления характеристики.
    Включает ID характеристики.
    """
    id: int

    class Config:
        """
        Конфигурация для работы с объектами, используя ORM (объектно-реляционное отображение).
        """
        orm_mode = True

