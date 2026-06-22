from __future__ import annotations

import os

from argon2 import PasswordHasher, Type
from argon2.exceptions import VerifyMismatchError

from ..config import settings

_hasher = PasswordHasher(
    time_cost=settings.argon2_time_cost,
    memory_cost=settings.argon2_memory_cost,
    parallelism=settings.argon2_parallelism,
    hash_len=settings.argon2_hash_len,
    salt_len=settings.argon2_salt_len,
    type=Type.ID,
)


def hash_master_password(password: str) -> bytes:
    return _hasher.hash(password).encode("utf-8")


def verify_master_password(hash_value: bytes, password: str) -> bool:
    try:
        return _hasher.verify(hash_value.decode("utf-8"), password)
    except VerifyMismatchError:
        return False
