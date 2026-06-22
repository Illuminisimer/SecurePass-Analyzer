from __future__ import annotations

import asyncio
import os
from typing import Tuple

import requests

from ..config import settings
from .analysis import PasswordStrengthAnalyzer

_analyzer = PasswordStrengthAnalyzer()


async def get_ai_assistant_response(client_hashed_input: str, privacy_mode: bool) -> Tuple[str, str]:
    if settings.openai_api_key.get_secret_value():
        try:
            return await _call_openai_assistant(client_hashed_input, privacy_mode)
        except Exception:
            pass

    return _local_assistant_response(client_hashed_input), "local"


async def _call_openai_assistant(client_hashed_input: str, privacy_mode: bool) -> Tuple[str, str]:
    prompt = (
        "You are a security assistant. The user has submitted a hashed input string. "
        "Offer general password hygiene recommendations without attempting to reverse the hash. "
        "Use the hashed data only to acknowledge a unique request. "
        f"Hashed input: {client_hashed_input}. Privacy mode: {privacy_mode}."
    )
    response = await asyncio.to_thread(
        requests.post,
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.openai_api_key.get_secret_value()}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.openai_model,
            "messages": [
                {"role": "system", "content": "You are a security assistant."},
                {"role": "user", "content": prompt},
            ],
            "max_tokens": 300,
        },
        timeout=20,
    )
    response.raise_for_status()
    data = response.json()
    choice = data.get("choices", [{}])[0]
    return choice.get("message", {}).get("content", "No response."), "openai"


def _local_assistant_response(client_hashed_input: str) -> str:
    recommendation = _analyzer._score_rule_based("A1!examplePassword", [])  # type: ignore[arg-type]
    return (
        "OpenAI integration is not configured. Here is a general security assistant reply:\n"
        "- Use a unique passphrase of at least 16 characters.\n"
        "- Include uppercase, lowercase, digits, and special chars.\n"
        "- Avoid reusing passwords or passwords based on personal data.\n"
        "- Enable 2FA on accounts and store emergency backup codes securely.\n"
        f"- Session fingerprint: {client_hashed_input[:12]}...\n"
        f"- Local score guideline sample: {recommendation}/100."
    )
