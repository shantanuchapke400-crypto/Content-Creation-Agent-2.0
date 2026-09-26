import os
from datetime import datetime, timedelta, timezone

import jwt
from django.contrib.auth import authenticate
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()

JWT_SECRET = os.getenv("JWT_SECRET", "dev-only-secret-change-me")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60


class AuthService:
    """Handles CreatorOS authentication and JWT tokens."""

    @staticmethod
    def create_access_token(user_id: int) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=JWT_EXPIRATION_MINUTES
        )

        payload = {
            "sub": str(user_id),
            "exp": expires_at,
        }

        return jwt.encode(
            payload,
            JWT_SECRET,
            algorithm=JWT_ALGORITHM,
        )

    @staticmethod
    def verify_token(token: str) -> int:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )

        return int(payload["sub"])


auth_service = AuthService()