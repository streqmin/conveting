from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomSignupForm(SignupForm):
    profile_image = forms.ImageField(label="프로필 이미지", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"] = forms.CharField(label="사용자명", max_length=30)

    class Meta:
        fields = ["username", "email", "profile_image", "password1", "password2"]

    def save(self, request):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password1"]
        email = self.cleaned_data.get("email")
        profile_image = self.cleaned_data.get("profile_image")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            profile_image=profile_image,
            social_type=User.SocialType.EMAIL,
        )

        return user

class CustomLoginForm(forms.Form):
    username = forms.CharField(label="사용자명", max_length=30)
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)

class UserUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(label="프로필 이미지", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "사용자명"
        self.fields["email"].label = "이메일"

    class Meta:
        model = User
        fields = ["username", "email", "profile_image"]
