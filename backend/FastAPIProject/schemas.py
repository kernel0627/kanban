# Pydantic 的数据校验模型
from pydantic import BaseModel, Field, EmailStr
from typing import Optional , List

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}

class Token(BaseModel):
    access_token: str
    token_type: str


class BoardBase(BaseModel):
    title : str

class ListBase(BaseModel):
    title : str

class CardBase(BaseModel):
    content : str


class Cards(CardBase):
    id : int
    list_id : int
    order : int
    model_config = {"from_attributes": True}

class Lists(ListBase):
    id : int
    board_id : int
    order: int
    cards: List[Cards] = []
    model_config = {"from_attributes": True}

class Boards(BoardBase):
    id : int
    lists: List[Lists] = []
    model_config = {"from_attributes": True}

class CardCreate(CardBase):
    pass

class ListCreate(ListBase):
    pass

class BoardCreate(BoardBase):
    pass

