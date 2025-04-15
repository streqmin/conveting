import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin


User = get_user_model()


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
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, User.DoesNotExist):
        return None


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_user_from_jwt(request) or AnonymousUser())


class DisableSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # admin 페이지는 세션 허용
        if request.path.startswith("/admin/"):
            return response

        # 그 외는 세션 저장 무력화
        if hasattr(request, "session"):
            request.session.save = lambda: None

        return response
