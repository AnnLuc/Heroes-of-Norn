"""Модуль конфигурации приложения."""

from pydantic_settings import BaseSettings, SettingsConfigDict

DATABASE_URL = "sqlite:///./app.db"


class Settings(BaseSettings):
    """
    Класс настроек, считывающий конфигурацию из переменных окружения.

    Атрибуты:
        db_username (str): Имя пользователя базы данных.
        db_password (str): Пароль пользователя базы данных.
        db_host (str): Адрес хоста базы данных.
        db_port (int): Порт базы данных.
        db_name (str): Название базы данных.
        secret_key (str): Секретный ключ для JWT.
        algo (str): Алгоритм шифрования.
        access_token_expire_minutes (int): Время жизни токена доступа в минутах.
    """

    model_config = SettingsConfigDict(env_file=".env")
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    secret_key: str
    algo: str
    access_token_expire_minutes: int


settings = Settings()

