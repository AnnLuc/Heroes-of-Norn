# app/models/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from .database import Base

# Модель User (Пользователь)
class User(Base):
    """
    Модель для пользователей в системе.
    Связана с кампаниями и персонажами.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)  # Здесь будет храниться зашифрованный пароль

    # Связи
    campaigns = relationship('Campaign', back_populates='gm')
    characters = relationship('Character', back_populates='user')


# Модель Campaign (Кампания)
class Campaign(Base):
    """
    Модель для кампаний в системе.
    Каждая кампания привязана к пользователю (GM).
    """
    __tablename__ = 'campaigns'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)  # Добавлено описание кампании

    gm_id = Column(Integer, ForeignKey('users.id'))
    gm = relationship('User', back_populates='campaigns')

    characters = relationship('Character', back_populates='campaign')


# Модель Character (Персонаж)
class Character(Base):
    """
    Модель для персонажей в системе.
    Персонажи могут быть привязаны к кампаниям и пользователям.
    """
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    campaign_id = Column(Integer, ForeignKey('campaigns.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    campaign = relationship('Campaign', back_populates='characters')
    user = relationship('User', back_populates='characters')

    # Связи с атрибутами и навыками
    attributes = relationship('CharacterAttribute', back_populates='character')
    skills = relationship('CharacterSkill', back_populates='character')


# Модель CharacterRole (Роль персонажа в кампании)
class CharacterRole(Base):
    """
    Модель для ролей персонажей в кампаниях.
    Определяет, кто является GM и кто игрок.
    """
    __tablename__ = 'character_roles'

    id = Column(Integer, primary_key=True)

    character_id = Column(Integer, ForeignKey('characters.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))

    role = Column(String)  # Пусто для заполнения позже: "GM" или "Player"

    # Связи
    character = relationship('Character')
    user = relationship('User')
    campaign = relationship('Campaign')


# Таблица для характеристик
class Attribute(Base):
    """
    Модель для характеристик персонажей.
    Каждая характеристика имеет тип кубика (например, 1d4, 1d6).
    """
    __tablename__ = 'attributes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название характеристики
    dice_type = Column(String, nullable=False)  # Тип кубика для этой характеристики (например, 1d4, 1d6 и т.д.)
    value = Column(Integer, nullable=False, default=1)  # Добавляем значение по умолчанию

    # Связь с навыками
    skills = relationship("Skill", back_populates="attribute")
    character_attributes = relationship("CharacterAttribute", back_populates="attribute")


# Таблица для навыков
class Skill(Base):
    """
    Модель для навыков персонажей.
    Каждый навык привязан к конкретной характеристике.
    """
    __tablename__ = 'skills'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Название навыка
    attribute_id = Column(Integer, ForeignKey('attributes.id'), nullable=False)  # Ссылаемся на характеристику
    bonus = Column(Integer, default=0)  # Бонус навыка (по умолчанию 0)

    # Связь с характеристикой
    attribute = relationship("Attribute", back_populates="skills")
    character_skills = relationship("CharacterSkill", back_populates="skill")


# Связующая таблица для атрибутов персонажа
class CharacterAttribute(Base):
    """
    Модель для связи персонажа с его характеристиками.
    Каждая характеристика персонажа может иметь свое значение.
    """
    __tablename__ = 'character_attributes'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    attribute_id = Column(Integer, ForeignKey('attributes.id'))
    value = Column(Integer, default=1)  # Значение характеристики для персонажа

    character = relationship('Character', back_populates='attributes')
    attribute = relationship('Attribute', back_populates='character_attributes')


# Связующая таблица для навыков персонажа
class CharacterSkill(Base):
    """
    Модель для связи персонажа с его навыками.
    Каждый навык персонажа может иметь бонус.
    """
    __tablename__ = 'character_skills'

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'))
    skill_id = Column(Integer, ForeignKey('skills.id'))
    bonus = Column(Integer, default=0)  # Бонус для навыка конкретного персонажа

    character = relationship('Character', back_populates='skills')
    skill = relationship('Skill', back_populates='character_skills')

