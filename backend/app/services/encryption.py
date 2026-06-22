from __future__ import annotations

import base64
import os
from typing import Tuple

from Crypto.Cipher import AES
from Crypto.Hash import SHA256, HMAC
from Crypto.Protocol.KDF import HKDF
from Crypto.Random import get_random_bytes

from ..config import settings

AES_KEY_SIZE = 32
AES_NONCE_SIZE = 12
AES_TAG_SIZE = 16
HKDF_SALT_SIZE = 32


def derive_key(master_password: str, salt: bytes) -> bytes:
    return HKDF(
        master_password.encode("utf-8"),
        AES_KEY_SIZE,
        salt,
        SHA256,
        num_keys=1,
        context=b"securepass-vault-key",
    )


def derive_database_key(master_password: str, salt: bytes) -> bytes:
    return HKDF(
        master_password.encode("utf-8"),
        AES_KEY_SIZE,
        salt,
        SHA256,
        num_keys=1,
        context=b"securepass-db-key",
    )


def encrypt_value(plaintext: str, key: bytes) -> dict[str, str]:
    plaintext_bytes = plaintext.encode("utf-8")
    nonce = get_random_bytes(AES_NONCE_SIZE)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext_bytes)
    return {
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8"),
    }


def decrypt_value(ciphertext: str, nonce: str, tag: str, key: bytes) -> str:
    ciphertext_bytes = base64.b64decode(ciphertext)
    nonce_bytes = base64.b64decode(nonce)
    tag_bytes = base64.b64decode(tag)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce_bytes)
    plaintext = cipher.decrypt_and_verify(ciphertext_bytes, tag_bytes)
    return plaintext.decode("utf-8")


def secure_zero(data: bytearray) -> None:
    for i in range(len(data)):
        data[i] = 0
