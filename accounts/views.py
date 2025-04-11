import jwt
from django.conf import settings
from django.views import View
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

seoul_tz = ZoneInfo("Asia/Seoul")

User = get_user_model()


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
        return render(request, "accounts/login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is None:
            # 에러 내용과 함께 login 페이지 렌더링
            return HttpResponseBadRequest("아이디 또는 비밀번호가 올바르지 않습니다.")

        # JWT 생성
        payload = {
            "user_id": str(user.id),
            "username": user.username,
            "exp": datetime.now(seoul_tz) + timedelta(days=7),
            "iat": datetime.now(seoul_tz),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        response = JsonResponse({"message": "로그인 성공"})
        response.set_cookie("jwt", token, httponly=True, samesite="Lax")
        return response


class LogoutView(View):
    def post(self, request):
        response = JsonResponse({"message": "로그아웃 성공"})
        response.delete_cookie("jwt")
        return response
