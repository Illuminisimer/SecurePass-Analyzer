from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    master_password: str = Field(..., min_length=12)


class TokenResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str
    token_type: str = "bearer"
    expires_at: Optional[datetime]


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    master_password: str
    totp_code: str | None = None
    backup_code: str | None = None


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    email: EmailStr
    is_active: bool
    totp_enabled: bool
    created_at: datetime
    last_login_at: datetime | None


class VaultCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1)
    description: Optional[str] = None
