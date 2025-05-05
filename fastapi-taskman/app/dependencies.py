"""Модуль для зависимостей, связанных с пользователем и авторизацией."""

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Request
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.models.models import User
from app.models.database import get_db

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_current_user(request: Request, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Получает текущего пользователя на основе токена.
    
    Пытается извлечь токен из cookies или из заголовков запроса. Декодирует его и проверяет.
    Если токен валиден, возвращает пользователя из базы данных.
    """
    if not token:
        # Проверяем токен в cookies
        token = request.cookies.get("access_token")
        print(f"Token from cookies: {token}")

    if not token:
        raise HTTPException(status_code=401, detail="Токен не предоставлен")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
    except JWTError as exc:
        raise HTTPException(status_code=401, detail="Неверный токен") from exc

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user

