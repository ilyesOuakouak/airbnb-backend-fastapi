from typing import Optional
from pydantic import BaseModel, EmailStr, constr, field_validator
from datetime import datetime, timezone

class UserBase(BaseModel):
    email: EmailStr
    first_name: constr(min_length=2, max_length=50)
    last_name: constr(min_length=2, max_length=50)

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=72)
    created_at: datetime

    @field_validator("created_at")
    def validate_created_at(cls, value):
        """Ensure created_at is >= current UTC time."""
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        if value < now:
            raise ValueError("created_at must be greater than or equal to the current time")

        return value

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=72)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"