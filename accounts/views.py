import jwt
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.views import View
from django.views.generic import UpdateView
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.models import Site
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+
from allauth.socialaccount.adapter import get_adapter
from allauth.account.utils import perform_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.helpers import render_authentication_error
from allauth.socialaccount.providers.oauth2.client import OAuth2Error

from .forms import UserUpdateForm
from .tokens import generate_tokens_for_user

seoul_tz = ZoneInfo("Asia/Seoul")

User = get_user_model()


class AdminJWTLoginView(View):
    def get(self, request):
        return render(request, "accounts/admin_login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None or not user.is_staff:
            return HttpResponseBadRequest("유효한 관리자 계정이 아닙니다.")

        access_token, refresh_token = generate_tokens_for_user(user)

        response = redirect("/admin/")
        response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Lax")

        return response


def index(request):
    return render(request, "accounts/index.html")


class MyPageView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "accounts/mypage.html"
    success_url = reverse_lazy("mypage")

    def get_object(self):
        user = self.request.user
        print(user)
        if not user.is_authenticated:
            raise PermissionDenied("로그인이 필요한 페이지입니다.")
        return user


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


class JWTLoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html")  # 로그인 폼

    def post(self, request):
        login_id = request.POST.get("login")  # username 또는 email
        password = request.POST.get("password")

        user = authenticate(request, username=login_id, password=password)
        if user is None:
            return HttpResponseBadRequest("아이디 또는 비밀번호가 올바르지 않습니다.")

        # 로그인 수행 (세션은 사용되지 않지만 로그인 signal은 발생시킴)
        perform_login(request, user, email_verification="optional")

        # JWT 발급
        access_token, refresh_token = generate_tokens_for_user(user)

        response = redirect("/")
        response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
        response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Lax")
        return response


class SocialLoginCallbackView(View):
    adapter_class = None

    def get(self, request):
        if self.adapter_class is None:
            return HttpResponseBadRequest("adapter_class가 정의되지 않았습니다.")

        try:
            # 1. provider adapter 생성
            provider_adapter = self.adapter_class(request)
            provider = provider_adapter.get_provider()
            provider_id = provider.id
            site = Site.objects.get_current(request)

            # 2. SocialApp 확인
            try:
                app = SocialApp.objects.get(provider=provider_id, sites=site)
            except SocialApp.DoesNotExist:
                return HttpResponseBadRequest(
                    f"SocialApp이 '{provider_id}'와 '{site}'에 대해 설정되지 않았습니다."
                )

            # 3. 토큰 및 사용자 정보 획득
            client = provider_adapter.get_client(request, app)
            code = request.GET.get("code")
            token = client.get_access_token(code)
            sociallogin = provider_adapter.complete_login(request, app, token, response=token)

            # 4. 사용자 생성 or 조회 (AccountAdapter 활용)
            user = get_adapter(request).save_user(request, sociallogin)

            # 5. JWT 발급 및 쿠키 저장
            access_token, refresh_token = generate_tokens_for_user(user)

            response = redirect("/")
            response.set_cookie("access_token", access_token, httponly=True, samesite="Lax")
            response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="Lax")
            return response

        except OAuth2Error as e:
            return render_authentication_error(request, provider.id, exception=e)
