import time
import jwt

from typing import Dict
from app.config import settings


def signJWT(user_id: int, expires_in_seconds: int) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "iat": time.time(),
        "exp": time.time() + expires_in_seconds
    }
    token = jwt.encode(payload, settings.secret_key,
                       algorithm=settings.algorithm)

    return token


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        raise Exception("JWTError: token is not decoded!")
