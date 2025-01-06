from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta, timezone
from typing import Annotated
from models import Users
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from starlette import status
from schemas import CreateUserRequest, Token
from dependencies import db_dependency, bcrypt_context, user_dependency
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
ALGORITHM = os.getenv("AUTH_ALGORITHM")

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return None
    if not bcrypt_context.verify(password, user.hashed_password):
        return None
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_new_client(
        db: db_dependency,
        create_user_request: CreateUserRequest):
    create_user_model = Users(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role="client"
    )

    if db.query(Users).filter(Users.username == create_user_model.username).first() is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    db.add(create_user_model)
    db.commit()

    return create_user_model

@router.post("/token", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Wrong username or password')

    token = create_access_token(user.username, user.user_id, user.role, timedelta(minutes=180))

    return {
        'access_token': token,
        'token_type': 'bearer'
    }

@router.get("/detail", status_code=status.HTTP_200_OK)
def get_user_detail(user: user_dependency):
    return {
    "user_id": user["id"],
    "username": user["username"],
    "role": user["role"]
    }