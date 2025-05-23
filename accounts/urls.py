from django.urls import path, include
from accounts.views import JWTLoginView, JWTLogoutView, SocialLoginCallbackView, MyPageView
from accounts.kakao_adapter import CustomKakaoOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

urlpatterns = [
    path("login/", JWTLoginView.as_view(), name="login"),
    path("logout/", JWTLogoutView.as_view(), name="logout"),
    path("mypage/", MyPageView.as_view(), name="mypage"),
    path(
        "kakao/login/callback/",
        type(
            "KakaoJWTCallbackView",
            (SocialLoginCallbackView,),
            {"adapter_class": CustomKakaoOAuth2Adapter},
        ).as_view(),
        name="kakao_jwt_callback",
    ),
    path(
        "google/login/callback/",
        type(
            "GoogleJWTCallbackView",
            (SocialLoginCallbackView,),
            {"adapter_class": GoogleOAuth2Adapter},
        ).as_view(),
        name="google_jwt_callback",
    ),
    path("", include("allauth.urls")),
]
