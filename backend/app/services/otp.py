from __future__ import annotations

import base64
import hashlib
import hmac
import io
import json
import os
from typing import Any

import pyotp
import qrcode
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from ..config import settings


def _serialize_backup_codes(codes: list[str]) -> str:
    return json.dumps([hashlib.sha256(code.encode("utf-8")).hexdigest() for code in codes])


def _deserialize_backup_codes(data: str) -> list[str]:
    try:
        return json.loads(data)
    except Exception:
        return []


def generate_totp_secret(user: User) -> tuple[str, str]:
    if not user.totp_secret:
        secret = pyotp.random_base32()
    else:
        secret = base64.b32encode(user.totp_secret).decode("utf-8")

    otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user.email,
        issuer_name="SecurePass Analyzer",
    )
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(otpauth_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    data_uri = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    return otpauth_url, data_uri


def verify_totp_code(user: User, code: str) -> bool:
    if not user.totp_secret:
        return False
    secret = base64.b32encode(user.totp_secret).decode("utf-8")
    totp = pyotp.TOTP(secret)
    return totp.verify(code, valid_window=1)


async def initialize_totp_for_user(user: User, master_password: str, session: AsyncSession) -> list[str]:
    if user.totp_secret is None:
        secret = pyotp.random_base32()
        user.totp_secret = base64.b32decode(secret)

    backup_codes = [hashlib.sha256(os.urandom(12)).hexdigest() for _ in range(8)]
    user.backup_codes = _serialize_backup_codes(backup_codes)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return backup_codes


async def verify_backup_code(user: User, code: str, session: AsyncSession) -> bool:
    if not user.backup_codes:
        return False
    hashed_codes = _deserialize_backup_codes(user.backup_codes)
    digest = hashlib.sha256(code.encode("utf-8")).hexdigest()
    if digest in hashed_codes:
        hashed_codes.remove(digest)
        user.backup_codes = json.dumps(hashed_codes)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return True
    return False
