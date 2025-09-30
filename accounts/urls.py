from django.urls import path, include
from accounts.views import JWTLoginView, JWTLogoutView, MyPageView

urlpatterns = [
    path("login/", JWTLoginView.as_view(), name="login"),
    path("logout/", JWTLogoutView.as_view(), name="logout"),
    path("mypage/", MyPageView.as_view(), name="mypage"),
    path("", include("allauth.urls")),
]
