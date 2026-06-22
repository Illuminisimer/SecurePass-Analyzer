from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

from ..database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    master_password_hash = Column(LargeBinary, nullable=False)
    master_password_salt = Column(LargeBinary, nullable=False)
    totp_secret = Column(LargeBinary, nullable=True)
    backup_codes = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_login_at = Column(DateTime, nullable=True)

    vaults = relationship("Vault", back_populates="owner")
    audit_logs = relationship("AuditLog", back_populates="user")
