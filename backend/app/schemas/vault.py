from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VaultCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=1)
    description: Optional[str] = None


class VaultResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    name: str
    description: Optional[str]
    created_at: str
    updated_at: str


class PasswordEntryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1)
    url: Optional[str] = None
    username: Optional[str] = None
    password: str = Field(..., min_length=8)
    notes: Optional[str] = None
    vault_id: int
    master_password: str = Field(..., min_length=12)


class PasswordEntryDecryptRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    entry_id: int
    vault_id: int
    master_password: str = Field(..., min_length=12)


class PasswordEntryDecryptResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    password: str


class PasswordEntryListItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    title: str
    url: Optional[str]
    username: Optional[str]
    strength_score: int
    breach_status: str
    tags: Optional[str]
    folder_path: Optional[str]
    created_at: str
    updated_at: str


class PasswordEntryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    title: str
    url: Optional[str]
    username: Optional[str]
    strength_score: int
    breach_status: str
    tags: Optional[str]
    folder_path: Optional[str]
    created_at: str
    updated_at: str
