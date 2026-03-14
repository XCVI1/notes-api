from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

class NoteCreate(BaseModel):
    title: str
    content: str
    is_public: bool = False


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_public: Optional[bool] = None

class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str
    is_public: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
