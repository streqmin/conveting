import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError
from zoneinfo import ZoneInfo


User = get_user_model()
seoul_tz = ZoneInfo("Asia/Seoul")


def get_user_from_jwt(request):
    token = request.COOKIES.get("access_token")
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "access":
            return None
        user = User.objects.get(id=payload.get("user_id"))
        return user
    except (ExpiredSignatureError, InvalidTokenError, User.DoesNotExist):
        return None


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user_from_jwt(request) or AnonymousUser())
