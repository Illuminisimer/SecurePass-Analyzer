from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

from ..schemas.assistant import AssistantRequest, AssistantResponse
from ..services.assistant import get_ai_assistant_response

router = APIRouter(prefix="/api/assistant", tags=["assistant"])
logger = logging.getLogger(__name__)


@router.post("/query", response_model=AssistantResponse)
async def assistant_query(request: AssistantRequest) -> AssistantResponse:
    try:
        response, source = await get_ai_assistant_response(request.client_hashed_input, request.privacy_mode)
        return AssistantResponse(
            assistant_response=response,
            source=source,
            conversation_id=request.conversation_id,
        )
    except Exception:
        logger.exception("Assistant query failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Assistant service unavailable",
        )
