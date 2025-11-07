from passlib.hash import bcrypt
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.core.auth import create_access_token

def authenticate_user(db: Session, email: EmailStr, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt.verify(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email or Password !")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}