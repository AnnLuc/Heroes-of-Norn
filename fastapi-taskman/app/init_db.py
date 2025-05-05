"""Модуль для инициализации базы данных и создания таблиц."""

from app.models.database import Base, engine
from app.models import models  # Импорт всех моделей для корректного создания таблиц

def init() -> None:
    """
    Инициализирует базу данных, создавая все необходимые таблицы.
    """
    print("Создание таблиц...")
    Base.metadata.create_all(bind=engine)
    print("Таблицы созданы.")

if __name__ == "__main__":
    init()

