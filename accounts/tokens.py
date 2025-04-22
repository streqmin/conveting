import jwt
from datetime import datetime, timedelta
from django.conf import settings
from zoneinfo import ZoneInfo

seoul_tz = ZoneInfo("Asia/Seoul")


def generate_tokens_for_user(user):
    now = datetime.now(tz=seoul_tz)

    access_payload = {
        "user_id": str(user.id),
        "username": user.username,
        "exp": now + timedelta(minutes=15),
        "iat": now,
        "type": "access",
    }

    refresh_payload = {
        "user_id": str(user.id),
        "exp": now + timedelta(days=7),
        "iat": now,
        "type": "refresh",
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    return access_token, refresh_token
