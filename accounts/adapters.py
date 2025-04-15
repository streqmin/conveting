from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialLogin

User = get_user_model()


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin: SocialLogin, form=None):
        user = sociallogin.user

        provider = sociallogin.account.provider
        uid = sociallogin.account.uid

        extra_data = sociallogin.account.extra_data
        nickname = extra_data.get("nickname") or extra_data.get("name") or "소셜사용자"

        try:
            return User.objects.get(social_type=provider, social_id=uid)
        except User.DoesNotExist:
            pass

        user = User.objects.create_social_user(
            username=nickname,
            social_type=provider,
            social_id=uid,
            email=extra_data.get("email", None),
            profile_image=extra_data.get("picture", None),
        )
        sociallogin.user = user
        return user
