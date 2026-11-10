from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, UserLogin
from security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
    User.username == user.username
    ).first()
    existing_email = db.query(User).filter(
    User.email == user.email
    ).first()
    
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    hashed = hash_password(user.password)
    new_user = User(
        username = user.username,
        email = user.email,
        hashed_password = hashed
    )
    db.add(new_user)
    db.commit()
    return {
            "message": "User registered successfully",
            "username": new_user.username
        }
@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    searched_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not searched_user or not verify_password(
        user.password, searched_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    access_token = create_access_token(
        data={"sub": searched_user.username}
    )
    return {
    "access_token": access_token,
    "token_type": "bearer"
    }
@router.get("/me")
def read_current_user(
    current_user: str = Depends(get_current_user)
):
    return {
        "message": "You are authenticated!",
        "username": current_user
    }