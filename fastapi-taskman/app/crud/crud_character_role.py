# app/crud/crud_character_role.py

"""
Модуль для работы с ролями персонажей в базе данных.
Предоставляет CRUD-операции для создания и получения ролей персонажей.
"""

from sqlalchemy.orm import Session
from app.models.models import CharacterRole
from app.schemas.character_role import CharacterRoleCreate

def create_character_role(db: Session, role_data: CharacterRoleCreate) -> CharacterRole:
    """
    Создаёт новую роль для персонажа и сохраняет её в базе данных.
    
    Аргументы:
    db (Session): объект сессии для взаимодействия с базой данных.
    role_data (CharacterRoleCreate): данные для создания новой роли персонажа.

    Возвращает:
    CharacterRole: созданная роль персонажа.
    """
    new_role = CharacterRole(
        role=role_data.role,
        character_id=role_data.character_id,
        user_id=role_data.user_id,
        campaign_id=role_data.campaign_id,
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

