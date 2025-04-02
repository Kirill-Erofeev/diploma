# # a = b'------WebKitFormBoundaryhnL1F7BklE6rRnan\r\nContent-Disposition: form-data; name="audio"; filename="audio.wav"\r\nContent-Type: audio/wav\r\n\r\n\x1aE\xdf\xa3\x9fB\x86\x81\x01B\xf7\x81\x01B\xf2\x81\x04B\xf3\x81\x08B\x82\x84webmB\x87\x81\x04B\x85\x81\x02\x18S\x80g\x01\xff\xff\xff\xff\xff\xff\xff\x15I\xa9f\x99*\xd7\xb1\x83\x0fB@M\x80\x86ChromeWA\x86Chrome\x16T\xaek\xbf\xae\xbd\xd7\x81\x01s\xc5\x87]\xc2l6{\xd16\x83\x81\x02\x86\x86'
# # # print(a[a.find(b"Content-Type: ")+len(b"Content-Type: "):])
# # with open('audio_file.wav', 'rb') as file:
# #     binary_data = file.read()
# # # print(binary_data[:])
# # from datetime import datetime

# # current_datetime = datetime.now()
# # current_datetime.microsecond = 0
# # print(current_datetime)

# print([] == None)


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Настройки JWT
SECRET_KEY = "your_secret_key"  # Секретный ключ (замени на свой)
ALGORITHM = "HS256"  # Алгоритм шифрования
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Время жизни токена

# Имитируем базу данных пользователей
fake_users_db = {
    "user1": {
        "username": "user1",
        "full_name": "Иван Иванов",
        "email": "ivan@example.com",
        "hashed_password": "$2b$12$aAaxL5QFqWX.WT3MgOXWgOXL5/TMo04p2uFlRJweqdeNBRsXUq8gK",  # пароль: secret
    }
}

# Настройка хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 схема для авторизации
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Модель пользователя
class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None

# Модель пользователя в БД
class UserInDB(User):
    hashed_password: str

# Модель токена
class Token(BaseModel):
    access_token: str
    token_type: str

# Функция хеширования пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Функция поиска пользователя в "базе данных"
def get_user(username: str):
    user = fake_users_db.get(username)
    if user:
        return UserInDB(**user)

# Функция аутентификации пользователя
def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Функция генерации JWT-токена
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# API
app = FastAPI()

# 🔑 **Эндпоинт авторизации**
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": user.username}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

# 🔍 **Функция получения текущего пользователя из токена**
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный токен")

    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    return user

# 🔎 **Эндпоинт получения информации о текущем пользователе**
@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
