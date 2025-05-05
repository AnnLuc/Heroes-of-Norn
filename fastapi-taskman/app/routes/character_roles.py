# app/routes/character_roles.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.character_role import CharacterRole, CharacterRoleCreate
from app.crud import crud_character_role

router = APIRouter(
    prefix="/character_roles",
    tags=["Character Roles"]
)

# Роуты для работы с ролями персонажей

@router.post("/", response_model=CharacterRole)
def create_character_role(role_data: CharacterRoleCreate, db: Session = Depends(get_db)):
    """
    Создаёт роль персонажа.

    :param role_data: Данные для создания роли персонажа
    :param db: Сессия базы данных
    :return: Созданная роль персонажа
    """
    return crud_character_role.create_character_role(db, role_data)
