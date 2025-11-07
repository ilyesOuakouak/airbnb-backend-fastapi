from typing import List

from app.core.auth import get_current_user
from app.core.database import get_db
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, TokenResponse, UserLogin
from passlib.hash import bcrypt
from app.services.user_service import authenticate_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == user.email).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already exist !!")

    password_to_hash = user.password[:72]
    print(f"Password length before hash: {len(password_to_hash)}")
    hashed_password = bcrypt.hash(password_to_hash)

    new_user = User(
        email=str(user.email),
        hashed_password=hashed_password,
        last_name=user.last_name,
        first_name=user.first_name,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {"id": new_user.id, "email": new_user.email}


@router.get("/me", status_code=status.HTTP_200_OK)
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name
    }


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found !")

    return user


@router.get("/list", response_model=List[UserResponse],  status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return users


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    return authenticate_user(db, user.email, user.password)


