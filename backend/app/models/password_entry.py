from __future__ import annotations

from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, LargeBinary,
                        String, Text)
from sqlalchemy.orm import relationship

from ..database.connection import Base


class PasswordEntry(Base):
    __tablename__ = "password_entries"

    id = Column(Integer, primary_key=True, index=True)
    vault_id = Column(Integer, ForeignKey("vaults.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    url = Column(String(512), nullable=True)
    username = Column(String(255), nullable=True)
    password_ciphertext = Column(LargeBinary, nullable=False)
    password_nonce = Column(LargeBinary, nullable=False)
    password_tag = Column(LargeBinary, nullable=False)
    notes_ciphertext = Column(LargeBinary, nullable=True)
    notes_nonce = Column(LargeBinary, nullable=True)
    notes_tag = Column(LargeBinary, nullable=True)
    strength_score = Column(Integer, default=0, nullable=False)
    breach_status = Column(String(32), default="CLEAN", nullable=False)
    tags = Column(String(512), nullable=True)
    folder_path = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    vault = relationship("Vault", back_populates="entries")
