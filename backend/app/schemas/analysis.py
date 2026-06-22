from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class AnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    password: str = Field(..., min_length=1)
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    dob: Optional[str] = None


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    score: int = Field(..., ge=0, le=100)
    grade: str
    entropy: float
    reasons: List[str]
    suggestions: List[str]
    ml_confidence: float = Field(..., ge=0.0, le=1.0)
    common_password: bool
    personal_info_matches: List[str]
