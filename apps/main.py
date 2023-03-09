from datetime import datetime
from enum import Enum
from urllib.request import Request
from pydantic import BaseModel, Field
from typing import List, Optional, Union
# Показ ошибок на сервере
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi.responses import JSONResponse

from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.database import User


app = FastAPI(
    title="Trading App"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)































#
# async def common_parameters(
#     q: Union[str, None] = None, skip: int = 0, limit: int = 100
# ):
#     return {"q": q, "skip": skip, "limit": limit}
#
#
# @app.get("/items/")
# async def read_items(commons: dict = Depends(common_parameters)):
#     return commons
#
#
# @app.get("/users/")
# async def read_users(commons: dict = Depends(common_parameters)):
#     return commons
#
#
# # Показывает ошибке на сервере
# @app.exception_handler(ValidationError)
# async def validation_exception_handler(request: Request, exc: ValidationError):
#     return JSONResponse(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content=jsonable_encoder({"detail": exc.errors()}),
#     )
#
# # база данных пользователей
# fake_users = [
#     {"id": 1, "role": "admin", "name": "Bob"},
#     {"id": 2, "role": "investor", "name": "John"},
#     {"id": 3, "role": "trader", "name": "Matt"},
#     {"id": 4, "role": "investor", "name": "Dastan", "degree": [
#         {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"}
#     ]}
# ]
#
#
# # Создает у пользователя какие есть должности
# class DegreeType(Enum):
#     newbie = "newbie"
#     expert = "expert"
#
#
# # Дополнительный класс для пользователя
# class Degree(BaseModel):
#     id: int
#     created_at: datetime
#     type_degree: DegreeType
#
#
# # Пользователи
# class User(BaseModel):
#     id: int   # ID пользователя
#     role: str # роль
#     name: str # имя
#     degree: Optional[List[Degree]]  # Optional это чтоб class DegreeType(Enum) не ругался что поля не заполнено, а дает null.
#
#
# # URLS
# @app.get("/users/{user_id}", response_model=List[User])
# def get_user(user_id: int):
#     return [user for user in fake_users if user.get("id") == user_id]
#
#
# # база данных какого нибудь данных
# fake_trades = [
#     {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
#     {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12},
# ]
#
#
# # Пагинация
# @app.get("/trades")
# def get_trades(limit: int = 1, offset: int = 0):
#     return fake_trades[offset:][:limit]
#
#
# # база данных еще пользователей
# fake_users2 = [
#     {"id": 1, "role": "admin", "name": "Bob"},
#     {"id": 2, "role": "investor", "name": "John"},
#     {"id": 3, "role": "trader", "name": "Matt"},
# ]
#
#
# # создание или же переименования имен в бд с fake_users2
# @app.post("/users/{user_id}")
# def change_user_name(user_id: int, new_name: str):
#     current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
#     current_user["name"] = new_name
#     return {"status": 200, "data": current_user}
#
#
# # модель для Trade
# class Trade(BaseModel):
#     id: int
#     user_id: int
#     currency: str = Field(max_length=200)
#     side: str
#     price: float = Field(ge=0) # Field(ge=0) равно или не меньше 0. можно иногда написать -1 по этому используется Field(ge=0)
#     amount: float
#
#
# # добовление или изминения данных
# @app.post("/trades")
# def add_trades(trades: List[Trade]):
#     fake_trades.extend(trades)
#     return {"status": 200, "data": fake_trades}
