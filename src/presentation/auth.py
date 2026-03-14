import os
from typing import Optional

from fastapi import Header, HTTPException, status


def _extract_bearer_token(authorization: Optional[str]) -> Optional[str]:
    if not authorization:
        return None
    if authorization.lower().startswith("bearer "):
        return authorization.split(" ", 1)[1].strip()
    return None


def verify_api_key(
    authorization: Optional[str] = Header(default=None),
    x_api_key: Optional[str] = Header(default=None),
) -> str:
    expected = os.getenv("VIDEO_GAME_LIBRARY_API_KEY", "dev-key")
    token = _extract_bearer_token(authorization) or x_api_key
    if not token or token != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )
    return token
