# app/schemas/character_role.py

from pydantic import BaseModel

# Модели для ролей персонажей в кампаниях
# Этот модуль содержит схемы для работы с ролями персонажей.

class CharacterRoleBase(BaseModel):
    """
    Базовая модель для роли персонажа.
    Содержит только поле для роли.
    """
    role: str

class CharacterRoleCreate(CharacterRoleBase):
    """
    Модель для создания роли персонажа.
    Расширяет базовую модель, добавляя идентификаторы персонажа, пользователя и кампании.
    """
    character_id: int
    user_id: int
    campaign_id: int

class CharacterRole(CharacterRoleBase):
    """
    Модель для представления роли персонажа в кампании.
    Включает идентификаторы персонажа, пользователя и кампании.
    """
    id: int
    character_id: int
    user_id: int
    campaign_id: int

    class Config:
        """
        Конфигурация для использования атрибутов при конвертации объектов.
        """
        from_attributes = True

