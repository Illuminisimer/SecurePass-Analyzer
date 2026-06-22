from __future__ import annotations

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings
from ..database.connection import async_session
from ..models.user import User
from ..schemas.auth import (LoginRequest, TokenResponse, UserCreateRequest,
                            UserProfileResponse)
from ..services.jwt_utils import create_access_token, verify_access_token
from ..services.otp import verify_backup_code, verify_totp_code
from ..services.password import verify_master_password
from ..services.vault import (create_default_vault, create_user,
                              get_user_by_email)

router = APIRouter(prefix="/api/auth", tags=["authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


async def authenticate_user(email: str, password: str, session: AsyncSession):
    user = await get_user_by_email(email, session)
    if user is None:
        return None
    if not verify_master_password(user.master_password_hash, password):
        return None
    return user


@router.post("/register", response_model=TokenResponse)
async def register_user(request: UserCreateRequest, session: AsyncSession = Depends(get_db)) -> TokenResponse:
    existing = await get_user_by_email(request.email, session)
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user = await create_user(request.email, request.master_password, session)
    await create_default_vault(user, session)
    user.last_login_at = datetime.utcnow()
    session.add(user)
    await session.commit()
    await session.refresh(user)
    access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    return TokenResponse(access_token=access_token, expires_at=None)


@router.post("/login", response_model=TokenResponse)
async def login_user(request: LoginRequest, session: AsyncSession = Depends(get_db)) -> TokenResponse:
    user = await authenticate_user(request.email, request.master_password, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if user.totp_secret is not None:
        if request.totp_code and verify_totp_code(user, request.totp_code):
            pass
        elif request.backup_code and await verify_backup_code(user, request.backup_code, session):
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="TOTP code or backup code required for this account",
            )

    access_token = create_access_token(subject=str(user.id), expires_delta=timedelta(minutes=settings.access_token_expire_minutes))
    user.last_login_at = datetime.utcnow()
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return TokenResponse(access_token=access_token, expires_at=None)


@router.get("/me", response_model=UserProfileResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)) -> UserProfileResponse:
    return UserProfileResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        totp_enabled=current_user.totp_secret is not None,
        created_at=current_user.created_at,
        last_login_at=current_user.last_login_at,
    )


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    try:
        payload = verify_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
