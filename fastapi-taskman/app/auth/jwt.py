from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app import crud
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Токен истек или неверен")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Неверный токен")
        return db.query(User).filter(User.id == user_id).first()
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверный токен")



# Секретный ключ для подписи JWT
SECRET_KEY = "your-secret-key"  # ❗Замени на .env позже
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Можно возвращать user_id или email
    except JWTError:
        return None

