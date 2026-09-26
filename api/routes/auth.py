from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from core import django_setup
from users.models import User
from core.services.auth_service import auth_service


router = APIRouter()


class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/auth/register")
def register(request: RegisterRequest):
    if User.objects.filter(username=request.username).exists():
        raise HTTPException(
            status_code=400,
            detail="Username already exists.",
        )

    if User.objects.filter(email=request.email).exists():
        raise HTTPException(
            status_code=400,
            detail="Email already exists.",
        )

    user = User.objects.create_user(
        username=request.username,
        email=request.email,
        password=request.password,
    )

    token = auth_service.create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }


@router.post("/auth/login")
def login(request: LoginRequest):
    user = User.objects.filter(
        username=request.username
    ).first()

    if not user or not user.check_password(request.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password.",
        )

    token = auth_service.create_access_token(user.id)

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
    }