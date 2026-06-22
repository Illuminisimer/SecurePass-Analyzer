from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TotpSetupResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    otpauth_url: str
    qrcode_data_uri: str


class TotpVerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    master_password: str = Field(..., min_length=12)
    totp_code: str = Field(..., min_length=6, max_length=6)


class TotpLoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    master_password: str = Field(..., min_length=12)
    totp_code: str | None = None
    backup_code: str | None = None


class BackupCodesResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    backup_codes: list[str]
