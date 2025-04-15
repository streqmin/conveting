from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.providers.kakao.provider import KakaoProvider


class CustomKakaoOAuth2Adapter(KakaoOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        access_token = token["access_token"]
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        response = get_adapter().get_requests_session().get(self.profile_url, headers=headers)
        response.raise_for_status()
        extra_data = response.json()

        return self.get_provider().sociallogin_from_response(request, extra_data)
