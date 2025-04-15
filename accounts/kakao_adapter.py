from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.kakao.provider import KakaoProvider


class CustomKakaoOAuth2Adapter(OAuth2Adapter):
    provider_id = KakaoProvider.id
    access_token_url = "https://kauth.kakao.com/oauth/token"
    authorize_url = "https://kauth.kakao.com/oauth/authorize"
    profile_url = "https://kapi.kakao.com/v2/user/me"

    def complete_login(self, request, app, token, **kwargs):
        access_token = token["access_token"]  # token은 dict 타입
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        response = get_adapter().get_requests_session().get(self.profile_url, headers=headers)
        response.raise_for_status()
        extra_data = response.json()

        return self.get_provider().sociallogin_from_response(request, extra_data)
