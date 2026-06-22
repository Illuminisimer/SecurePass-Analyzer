from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Optional

from jose import JWTError, jwt

from ..config import settings


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    payload: Dict[str, str] = {
        "sub": subject,
        "exp": expire.isoformat(),
    }
    return jwt.encode(payload, settings.jwt_secret_key.get_secret_value(), algorithm=settings.jwt_algorithm)


def verify_access_token(token: str) -> Dict[str, str]:
    try:
        return jwt.decode(token, settings.jwt_secret_key.get_secret_value(), algorithms=[settings.jwt_algorithm])
    except JWTError as error:
        raise error
