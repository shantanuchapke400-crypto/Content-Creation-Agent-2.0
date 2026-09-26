
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core import django_setup
from core.services.auth_service import auth_service
from users.models import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:
        user_id = auth_service.verify_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token.",
        )

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=401,
            detail="User not found.",
        )