# app/models.py

from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    hashed_password: str
