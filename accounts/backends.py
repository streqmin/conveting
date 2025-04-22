import jwt
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from jwt import ExpiredSignatureError, InvalidTokenError

User = get_user_model()


class JWTAuthenticationBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        if request is None:
            return None

        token = request.COOKIES.get("access_token")
        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("type") != "access":
                return None

            user_id = payload.get("user_id")
            user = User.objects.get(id=user_id)
            return user if user.is_active else None

        except (ExpiredSignatureError, InvalidTokenError, User.DoesNotExist):
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
