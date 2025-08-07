from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    marketing_consent: Optional[bool] = False

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
    email_verified: bool
    status: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class EmailVerification(BaseModel):
    email: EmailStr

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
