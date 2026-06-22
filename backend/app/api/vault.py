from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.auth import get_current_user
from ..database.connection import async_session
from ..models.password_entry import PasswordEntry
from ..models.vault import Vault
from ..schemas.vault import (PasswordEntryDecryptRequest,
                             PasswordEntryDecryptResponse,
                             PasswordEntryListItem, PasswordEntryRequest,
                             PasswordEntryResponse, VaultCreateRequest,
                             VaultResponse)
from ..services.vault import (create_password_entry, create_vault,
                              decrypt_password_entry, get_vault_entries,
                              get_vaults_for_user)

router = APIRouter(prefix="/api/vault", tags=["vault"])


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


@router.post("/", response_model=VaultResponse)
async def create_vault_endpoint(
    request: VaultCreateRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> VaultResponse:
    vault = await create_vault(current_user, request.name, request.description, session)
    return VaultResponse(
        id=vault.id,
        name=vault.name,
        description=vault.description,
        created_at=vault.created_at.isoformat(),
        updated_at=vault.updated_at.isoformat(),
    )


@router.get("/", response_model=list[VaultResponse])
async def list_vaults(
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> list[VaultResponse]:
    vaults = await get_vaults_for_user(current_user, session)
    return [
        VaultResponse(
            id=vault.id,
            name=vault.name,
            description=vault.description,
            created_at=vault.created_at.isoformat(),
            updated_at=vault.updated_at.isoformat(),
        )
        for vault in vaults
    ]


@router.get("/{vault_id}/entries", response_model=list[PasswordEntryListItem])
async def list_vault_entries(
    vault_id: int,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> list[PasswordEntryListItem]:
    vault = await session.get(Vault, vault_id)
    if vault is None or vault.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vault not found")

    entries = await get_vault_entries(vault, session)
    return [
        PasswordEntryListItem(
            id=entry.id,
            title=entry.title,
            url=entry.url,
            username=entry.username,
            strength_score=entry.strength_score,
            breach_status=entry.breach_status,
            tags=entry.tags,
            folder_path=entry.folder_path,
            created_at=entry.created_at.isoformat(),
            updated_at=entry.updated_at.isoformat(),
        )
        for entry in entries
    ]


@router.post("/entry/decrypt", response_model=PasswordEntryDecryptResponse)
async def decrypt_entry(
    request: PasswordEntryDecryptRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> PasswordEntryDecryptResponse:
    vault = await session.get(Vault, request.vault_id)
    if vault is None or vault.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vault not found")

    entry = await session.get(PasswordEntry, request.entry_id)
    if entry is None or entry.vault_id != vault.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entry not found")

    password = await decrypt_password_entry(entry, request.master_password, current_user)
    return PasswordEntryDecryptResponse(password=password)


@router.post("/entry", response_model=PasswordEntryResponse)
async def create_entry(
    request: PasswordEntryRequest,
    current_user=Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    vault = await session.get(Vault, request.vault_id)
    if vault is None or vault.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vault not found")

    entry = await create_password_entry(
        current_user,
        vault,
        request.title,
        request.url,
        request.username,
        request.password,
        request.notes,
        request.master_password,
        session,
    )

    return PasswordEntryResponse(
        id=entry.id,
        title=entry.title,
        url=entry.url,
        username=entry.username,
        strength_score=entry.strength_score,
        breach_status=entry.breach_status,
        tags=entry.tags,
        folder_path=entry.folder_path,
        created_at=entry.created_at.isoformat(),
        updated_at=entry.updated_at.isoformat(),
    )
