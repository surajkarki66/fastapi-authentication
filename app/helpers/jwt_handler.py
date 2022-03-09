import time
import jwt

from typing import Dict
from app.config import settings


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, settings.secret_key,
                       algorithm=settings.algorithm)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
