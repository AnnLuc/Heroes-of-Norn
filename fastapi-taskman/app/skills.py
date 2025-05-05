# app/skill.py
"""Модуль инициализации характеристик и навыков в базе данных."""

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app.models.models import Attribute, Skill
from app.models.database import DATABASE_URL

# Установка соединения с базой данных
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

# Список характеристик и их значений (просто числовые значения от 1 до 5)
attributes = [
    {"name": "Физ форма", "value": 1},
    {"name": "Сноровка", "value": 1},
    {"name": "Восприятие", "value": 1},
    {"name": "Мудрость", "value": 1},
    {"name": "Интеллект", "value": 1},
    {"name": "Интуиция", "value": 1},
    {"name": "Харизма", "value": 1},
    {"name": "Сила воли", "value": 1},
    {"name": "Эмпатия", "value": 1},
]

# Список навыков и связанных с ними характеристик
skills = [
    {"name": "Атлетика", "attribute_name": "Физ форма", "bonus": 0},
    {"name": "Ратное дело", "attribute_name": "Физ форма", "bonus": 0},
    {"name": "Блокирование", "attribute_name": "Физ форма", "bonus": 0},
    {"name": "Рукопашный бой", "attribute_name": "Физ форма", "bonus": 0},
    {"name": "Выживание*", "attribute_name": "Физ форма", "bonus": 0},
    {"name": "Проворство", "attribute_name": "Сноровка", "bonus": 0},
    {"name": "Фехтование", "attribute_name": "Сноровка", "bonus": 0},
    {"name": "Скрытность", "attribute_name": "Сноровка", "bonus": 0},
    {"name": "Боевое искусство", "attribute_name": "Сноровка", "bonus": 0},
    {"name": "Уклонение", "attribute_name": "Сноровка", "bonus": 0},
    {"name": "Внимательность", "attribute_name": "Восприятие", "bonus": 0},
    {"name": "Стрелковое оружие", "attribute_name": "Восприятие", "bonus": 0},
    {"name": "Огнестрельное оружие", "attribute_name": "Восприятие", "bonus": 0},
    {"name": "Метание", "attribute_name": "Восприятие", "bonus": 0},
    {"name": "Реакция", "attribute_name": "Восприятие", "bonus": 0},
    {"name": "Эрудиция", "attribute_name": "Мудрость", "bonus": 0},
    {"name": "Тактика", "attribute_name": "Мудрость", "bonus": 0},
    {"name": "Языки*", "attribute_name": "Мудрость", "bonus": 0},
    {"name": "Авторитет", "attribute_name": "Мудрость", "bonus": 0},
    {"name": "Ритуализм", "attribute_name": "Мудрость", "bonus": 0},
    {"name": "Знания", "attribute_name": "Интеллект", "bonus": 0},
    {"name": "Анализ", "attribute_name": "Интеллект", "bonus": 0},
    {"name": "Матрица", "attribute_name": "Интеллект", "bonus": 0},
    {"name": "Пиротехника", "attribute_name": "Интеллект", "bonus": 0},
    {"name": "Артефакторика", "attribute_name": "Интеллект", "bonus": 0},
    {"name": "Понимание", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Смекалка", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Чутьё", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Концептуализация", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Прорицание", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Убеждение", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Имитация", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Лидерство", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Обман", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Торг", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Давление", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Хладнокровие", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Решительность", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Превозмогание", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Концентрация", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Влияние", "attribute_name": "Эмпатия", "bonus": 0},
    {"name": "Оценка поведения", "attribute_name": "Эмпатия", "bonus": 0},
    {"name": "Выступление", "attribute_name": "Эмпатия", "bonus": 0},
    {"name": "Проницательность", "attribute_name": "Эмпатия", "bonus": 0},
    {"name": "Самоанализ", "attribute_name": "Эмпатия", "bonus": 0},
]


def add_attributes_and_skills():
    """Добавляет характеристики и навыки в базу данных, если их ещё нет."""
    try:
        for attr in attributes:
            existing_attr = session.query(Attribute).filter(
                Attribute.name == attr["name"]
            ).first()
            if not existing_attr:
                new_attribute = Attribute(
                    name=attr["name"],
                    dice_type="1d4",
                    value=attr["value"]
                )
                session.add(new_attribute)

        session.commit()

        for skill in skills:
            attribute = session.query(Attribute).filter(
                Attribute.name == skill["attribute_name"]
            ).first()
            if attribute:
                existing_skill = session.query(Skill).filter(
                    Skill.name == skill["name"]
                ).first()
                if not existing_skill:
                    new_skill = Skill(
                        name=skill["name"],
                        attribute_id=attribute.id,
                        bonus=skill["bonus"]
                    )
                    session.add(new_skill)

        session.commit()
        print("Данные успешно добавлены!")

    except IntegrityError:
        session.rollback()
        print("Ошибка добавления данных. Возможно, они уже есть в базе.")

    finally:
        session.close()


if __name__ == "__main__":
    add_attributes_and_skills()

    {"name": "Смекалка", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Чутьё", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Концептуализация", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Прорицание", "attribute_name": "Интуиция", "bonus": 0},
    {"name": "Убеждение", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Имитация", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Лидерство", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Обман", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Торг", "attribute_name": "Харизма", "bonus": 0},
    {"name": "Давление", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Хладнокровие", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Решительность", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Превозмогание", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Концентрация", "attribute_name": "Сила воли", "bonus": 0},
    {"name": "Влияние", "attribute_name": "Эмпатия", "bonus": 0},
    {"name": "Оценка поведения", "attribute_name": "Эмпатия", "bonus": 0},
    {"name": "Выступление", "attribute_name": "Эмпатия", "bonus": 0},
    {"name": "Проницательность", "attribute_name": "Эмпатия", "bonus": 0},
    {"name": "Самоанализ", "attribute_name": "Эмпатия", "bonus": 0},
]

# Функция для добавления данных в базу
def add_attributes_and_skills():
    try:
        # Добавление характеристик
        for attr in attributes:
            existing_attr = session.query(Attribute).filter(Attribute.name == attr["name"]).first()
            if not existing_attr:
                new_attribute = Attribute(
                    name=attr["name"],
                    dice_type="1d4",
                    value=attr["value"]
                )
                session.add(new_attribute)

        # Сохранение изменений характеристик
        session.commit()

        # Добавление навыков с бонусом
        for skill in skills:
            attribute = session.query(Attribute).filter(Attribute.name == skill["attribute_name"]).first()
            if attribute:
                existing_skill = session.query(Skill).filter(Skill.name == skill["name"]).first()
                if not existing_skill:
                    new_skill = Skill(
                        name=skill["name"],
                        attribute_id=attribute.id,
                        bonus=skill["bonus"]  # Добавляем бонус
                    )
                    session.add(new_skill)

        # Сохранение изменений навыков
        session.commit()

        print("Данные успешно добавлены!")

    except IntegrityError:
        session.rollback()
        print("Ошибка добавления данных. Возможно, эти данные уже есть в базе.")

    finally:
        session.close()

# Запуск добавления характеристик и навыков
if __name__ == "__main__":
    add_attributes_and_skills()

