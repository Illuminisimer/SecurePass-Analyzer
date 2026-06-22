from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class AssistantRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_hashed_input: str = Field(..., min_length=1)
    conversation_id: str | None = None
    privacy_mode: bool = False


class AssistantResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assistant_response: str
    source: str
    conversation_id: str | None = None
