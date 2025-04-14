from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .tokens import generate_tokens_for_user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def login(self, request, user):
        """
        세션 login은 생략하고 JWT만 발급하여 request에 저장
        """
        access_token, refresh_token = generate_tokens_for_user(user)
        request.jwt_access_token = access_token
        request.jwt_refresh_token = refresh_token
