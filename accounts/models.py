from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
import os


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("사용자명(username)은 반드시 입력해야 합니다.")

        username = self.model.normalize_username(username)

        user = self.model(username=username, **extra_fields)
        if password:
            user.password = make_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("슈퍼유저는 반드시 is_staff=True 이어야 합니다.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저는 반드시 is_superuser=True 이어야 합니다.")

        return self._create_user(username, password, **extra_fields)

    def create_social_user(self, username, social_type, social_id, **extra_fields):
        if not username:
            raise ValueError("사용자명(username)은 반드시 입력해야 합니다.")
        if not social_type:
            raise ValueError("소셜 타입은 반드시 지정해야 합니다.")
        if not social_id:
            raise ValueError("소셜 ID는 반드시 지정해야 합니다.")

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields["social_type"] = social_type
        extra_fields["social_id"] = social_id

        return self._create_user(username=username, password=None, **extra_fields)


def profile_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    unique_id = uuid.uuid4().hex[:8]
    new_filename = f"{instance.username}_{unique_id}.{ext}"
    return os.path.join("profile_images", new_filename)


class User(AbstractBaseUser, PermissionsMixin):
    class SocialType(models.TextChoices):
        EMAIL = "email", "Email"
        KAKAO = "kakao", "Kakao"
        GOOGLE = "google", "Google"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    profile_image = models.ImageField(upload_to=profile_image_upload_path, blank=True, null=True)
    social_type = models.CharField(
        max_length=20, choices=SocialType.choices, default=SocialType.EMAIL
    )
    social_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("user")
