from django.contrib import admin
from django.urls import path, include
from accounts.views import SocialLoginCallbackView, index
from accounts.kakao_adapter import CustomKakaoOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("api/auth/", include("accounts.urls")),
    path(
        "accounts/social/login/callback/", SocialLoginCallbackView.as_view(), name="social_callback"
    ),
    path(
        "accounts/kakao/login/callback/",
        type(
            "KakaoJWTCallbackView",
            (SocialLoginCallbackView,),
            {"adapter_class": CustomKakaoOAuth2Adapter},
        ).as_view(),
        name="kakao_jwt_callback",
    ),
    path(
        "accounts/google/login/callback/",
        type(
            "GoogleJWTCallbackView",
            (SocialLoginCallbackView,),
            {"adapter_class": GoogleOAuth2Adapter},
        ).as_view(),
        name="google_jwt_callback",
    ),
    path("accounts/", include("allauth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
