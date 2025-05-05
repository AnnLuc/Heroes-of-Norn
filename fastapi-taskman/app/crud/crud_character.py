# app/crud/crud_character.py

"""
Модуль для работы с персонажами в базе данных.
Предоставляет функции для создания, обновления, удаления и получения персонажей.
"""

from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
import random
from app.models.models import Character, CharacterAttribute, CharacterSkill, Attribute, Skill
from app.schemas.character import CharacterCreate, CharacterUpdate
from app.schemas.character_attribute import CharacterAttributeCreate
from app.schemas.character_skill import CharacterSkillCreate

# Получение всех персонажей
def get_characters(db: Session) -> List[Character]:
    return db.query(Character).all()

# Получение персонажа по ID
def get_character_by_id(db: Session, character_id: int):
    """
    Получает персонажа по ID, включая его атрибуты и навыки.

    Аргументы:
    db (Session): объект сессии для взаимодействия с базой данных.
    character_id (int): ID персонажа.

    Возвращает:
    Character: персонаж с указанным ID.
    """
    return db.query(Character) \
        .options(
            joinedload(Character.attributes).joinedload(CharacterAttribute.attribute).joinedload(Attribute.skills),
            joinedload(Character.skills).joinedload(CharacterSkill.skill)
        ) \
        .filter(Character.id == character_id) \
        .first()

# Получение персонажей по пользователю или кампании
def get_characters_by_user_or_campaign(db: Session, user_id: Optional[int] = None, campaign_id: Optional[int] = None) -> List[Character]:
    """
    Получает персонажей по ID пользователя или кампании.

    Аргументы:
    db (Session): объект сессии для взаимодействия с базой данных.
    user_id (Optional[int]): ID пользователя.
    campaign_id (Optional[int]): ID кампании.

    Возвращает:
    List[Character]: список персонажей.
    """
    query = db.query(Character)
    if user_id:
        query = query.filter(Character.user_id == user_id)
    if campaign_id:
        query = query.filter(Character.campaign_id == campaign_id)
    return query.all()

# Создание нового персонажа
def create_character(db: Session, character_data: CharacterCreate, user_id: int, campaign_id: int) -> Character:
    """
    Создаёт нового персонажа и его атрибуты и навыки.

    Аргументы:
    db (Session): объект сессии для взаимодействия с базой данных.
    character_data (CharacterCreate): данные для создания нового персонажа.
    user_id (int): ID пользователя.
    campaign_id (int): ID кампании.

    Возвращает:
    Character: созданный персонаж.
    """
    new_character = Character(
        name=character_data.name,
        description=character_data.description,
        user_id=user_id,
        campaign_id=campaign_id,
    )
    db.add(new_character)
    db.commit()
    db.refresh(new_character)

    # Атрибуты
    for attr_id, attr_value in character_data.attributes.items():
        character_attribute = CharacterAttribute(
            character_id=new_character.id,
            attribute_id=attr_id,
            value=attr_value
        )
        db.add(character_attribute)

    # Навыки
    for skill_id, bonus in character_data.skills.items():
        character_skill = CharacterSkill(
            character_id=new_character.id,
            skill_id=skill_id,
            bonus=bonus
        )
        db.add(character_skill)

    db.commit()
    db.refresh(new_character)
    return new_character

# Обновление персонажа
def update_character(db: Session, character_id: int, character_data: CharacterUpdate) -> Optional[Character]:
    """
    Обновляет данные персонажа, включая атрибуты и навыки.

    Аргументы:
    db (Session): объект сессии для взаимодействия с базой данных.
    character_id (int): ID персонажа.
    character_data (CharacterUpdate): новые данные для обновления.

    Возвращает:
    Character: обновлённый персонаж.
    """
    character = get_character_by_id(db, character_id)
    if not character:
        return None

    # Обновляем поля персонажа
    if character_data.name:
        character.name = character_data.name
    if character_data.description is not None:
        character.description = character_data.description

    # Обновляем характеристики
    if character_data.attributes:
        for attr_name, attr_value in character_data.attributes.items():
            # Ищем или создаём новый атрибут для персонажа
            attribute = db.query(Attribute).filter(Attribute.name == attr_name).first()
            if attribute:
                char_attr = db.query(CharacterAttribute).filter(
                    CharacterAttribute.character_id == character.id,
                    CharacterAttribute.attribute_id == attribute.id
                ).first()
                if char_attr:
                    char_attr.value = attr_value  # Обновляем значение
                else:
                    new_char_attr = CharacterAttribute(
                        character_id=character.id,
                        attribute_id=attribute.id,
                        value=attr_value
                    )
                    db.add(new_char_attr)

    # Обновляем навыки
    if character_data.skills:
        for skill_data in character_data.skills:
            skill = db.query(Skill).filter(Skill.name == skill_data.name).first()
            if skill:
                char_skill = db.query(CharacterSkill).filter(
                    CharacterSkill.character_id == character.id,
                    CharacterSkill.skill_id == skill.id
                ).first()
                if char_skill:
                    char_skill.bonus = skill_data.bonus  # Обновляем бонус
                else:
                    new_char_skill = CharacterSkill(
                        character_id=character.id,
                        skill_id=skill.id,
                        bonus=skill_data.bonus
                    )
                    db.add(new_char_skill)

    db.commit()
    db.refresh(character)
    return character

# Удаление персонажа
def delete_character(db: Session, character_id: int) -> Optional[Character]:
    """
    Удаляет персонажа из базы данных.

    Аргументы:
    db (Session): объект сессии для взаимодействия с базой данных.
    character_id (int): ID персонажа.

    Возвращает:
    Character: удалённый персонаж.
    """
    character = get_character_by_id(db, character_id)
    if not character:
        return None

    # Удаляем связи с атрибутами и навыками
    db.query(CharacterAttribute).filter(CharacterAttribute.character_id == character.id).delete()
    db.query(CharacterSkill).filter(CharacterSkill.character_id == character.id).delete()

    db.delete(character)
    db.commit()
    return character

# Бросок атрибута с учётом навыка
def roll_attribute(character: Character, attribute: str, skill: str = None) -> int:
    """
    Выполняет бросок атрибута с учётом бонуса от навыка.

    Аргументы:
    character (Character): персонаж, чьи атрибуты и навыки будут использоваться.
    attribute (str): название атрибута.
    skill (Optional[str]): название навыка.

    Возвращает:
    int: результат броска.
    """
    # Сначала получаем значение характеристики
    attribute_value = next((char_attr.value for char_attr in character.attributes if char_attr.attribute.name == attribute), 1)

    # Определяем тип кубика в зависимости от значения характеристики
    dice_type = {
        1: 4,  # 1d4
        2: 6,  # 1d6
        3: 8,  # 1d8
        4: 10,  # 1d10
        5: 12,  # 1d12
    }.get(attribute_value, 4)

    # Бросаем кубик
    dice_roll = random.randint(1, dice_type)

    # Если навык передан, прибавляем бонус
    bonus = 0
    if skill:
        skill_bonus = next(
            (char_skill.bonus for char_skill in character.skills if char_skill.skill.name == skill), 0
        )
        bonus += skill_bonus

    return dice_roll + bonus

# Получение персонажей по ID кампании
def get_characters_by_campaign_id(db: Session, campaign_id: int):
    return db.query(Character).filter(Character.campaign_id == campaign_id).all()
