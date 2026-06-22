from __future__ import annotations

import base64
import logging

import pyotp
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.auth import authenticate_user, get_current_user
from ..database.connection import async_session
from ..schemas.otp import (BackupCodesResponse, TotpLoginRequest,
                           TotpSetupResponse, TotpVerifyRequest)
from ..services.otp import (generate_totp_secret, initialize_totp_for_user,
                            verify_backup_code, verify_totp_code)
from ..services.password import verify_master_password

router = APIRouter(prefix="/api/auth/2fa", tags=["2fa"])
logger = logging.getLogger(__name__)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


@router.post("/setup", response_model=TotpSetupResponse)
async def setup_totp(current_user=Depends(get_current_user), session: AsyncSession = Depends(get_db)) -> TotpSetupResponse:
    if current_user.totp_secret is None:
        secret = pyotp.random_base32()
        current_user.totp_secret = base64.b32decode(secret)
        session.add(current_user)
        await session.commit()
        await session.refresh(current_user)

    otpauth_url, qrcode_data_uri = generate_totp_secret(current_user)
    return TotpSetupResponse(otpauth_url=otpauth_url, qrcode_data_uri=qrcode_data_uri)


@router.post("/enable", response_model=BackupCodesResponse)
async def enable_totp(request: TotpVerifyRequest, current_user=Depends(get_current_user), session: AsyncSession = Depends(get_db)) -> BackupCodesResponse:
    if not verify_master_password(current_user.master_password_hash, request.master_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Master password verification failed")

    if current_user.totp_secret is None or not verify_totp_code(current_user, request.totp_code):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid TOTP code")

    backup_codes = await initialize_totp_for_user(current_user, request.master_password, session)
    return BackupCodesResponse(backup_codes=backup_codes)


@router.post("/login")
async def totp_login(request: TotpLoginRequest, session: AsyncSession = Depends(get_db)):
    user = await authenticate_user(request.email, request.master_password, session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if user.totp_secret is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA not enabled for this account")

    if request.totp_code and verify_totp_code(user, request.totp_code):
        return {"status": "success"}

    if request.backup_code and await verify_backup_code(user, request.backup_code, session):
        return {"status": "success", "used_backup_code": request.backup_code}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid 2FA code or backup code")
