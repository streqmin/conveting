import jwt
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.sites.models import Site
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.models import SocialLogin, SocialApp
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount.providers.oauth2.client import OAuth2Error


from .tokens import generate_tokens_for_user

seoul_tz = ZoneInfo("Asia/Seoul")

User = get_user_model()


def index(request):
    return render(request, "accounts/index.html")


class SignUpView(View):
    def get(self, request):
        return render(request, "accounts/signup.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return HttpResponseBadRequest("아이디와 비밀번호는 필수입니다.")

        if User.objects.filter(username=username).exists():
            return HttpResponseBadRequest("이미 존재하는 사용자명입니다.")

        User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "회원가입 성공"}, status=201)


class LoginView(View):
    def get(self, request):
        return render(request, "account/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "아이디 또는 비밀번호가 올바르지 않습니다.")
            return render(request, "accounts/login.html", status=400)

        access_token, refresh_token = generate_tokens_for_user(user)

        response = JsonResponse({"message": "로그인 성공"})
        response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Lax")
        return response


class LogoutView(View):
    def post(self, request):
        response = JsonResponse({"message": "로그아웃 성공"})
        response.delete_cookie("jwt")
        return response


class TokenRefreshView(View):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return JsonResponse({"error": "Refresh token이 없습니다."}, status=400)

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({"error": "Refresh token이 만료되었습니다."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"error": "유효하지 않은 refresh token입니다."}, status=401)

        if payload.get("type") != "refresh":
            return JsonResponse({"error": "잘못된 토큰 타입입니다."}, status=400)

        user_id = payload.get("user_id")

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({"error": "존재하지 않는 유저입니다."}, status=404)

        now = datetime.now(tz=seoul_tz)
        new_access_payload = {
            "user_id": str(user.id),
            "username": user.username,
            "exp": now + timedelta(minutes=15),
            "iat": now,
            "type": "access",
        }
        new_access_token = jwt.encode(new_access_payload, settings.SECRET_KEY, algorithm="HS256")

        response = JsonResponse({"message": "access token 재발급 성공"})
        response.set_cookie("access_token", new_access_token, httponly=True, samesite="Lax")
        return response


class SocialLoginCallbackView(View):
    adapter_class = None  # 반드시 서브클래스에서 설정해야 함

    def get(self, request):
        if self.adapter_class is None:
            return HttpResponseBadRequest("Adapter가 정의되지 않았습니다.")

        try:
            adapter = self.adapter_class(request)
            provider = adapter.get_provider()
            provider_id = provider.id
            site = Site.objects.get_current(request)
            try:
                app = SocialApp.objects.get(provider=provider_id, sites=site)
            except SocialApp.DoesNotExist:
                return HttpResponseBadRequest(
                    f"No SocialApp found for provider '{provider_id}' and site '{site}'"
                )

            client = adapter.get_client(request, app)
            code = request.GET.get("code")

            token = client.get_access_token(code)
            sociallogin = adapter.complete_login(request, app, token, response=token)
            sociallogin.token = token
            sociallogin.state = SocialLogin.state_from_request(request)

            # DB에 유저 저장 (세션 login 없이 직접 저장)
            get_adapter(request).pre_social_login(request, sociallogin)
            sociallogin.lookup()

            user = sociallogin.user
            user.set_unusable_password()  # 소셜 로그인 전용 비밀번호 없음
            user.save()
            sociallogin.account.user = user
            sociallogin.account.save()

            access_token, refresh_token = generate_tokens_for_user(user)

            response = redirect("/")
            response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
            response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Lax")
            return response

        except OAuth2Error as e:
            return render_authentication_error(request, adapter.provider_id, exception=e)
