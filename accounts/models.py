from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_backends, load_backend
from django.utils.translation import gettext_lazy as _
from django.apps import apps
from django.core.exceptions import ImproperlyConfigured
from django.db import models
import uuid


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("이메일은 반드시 입력해야 합니다.")

        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)

        user = self.model(email=email, **extra_fields)
        if password:
            user.password = make_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("슈퍼유저는 반드시 is_staff=True 이어야 합니다.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("슈퍼유저는 반드시 is_superuser=True 이어야 합니다.")

        return self._create_user(email, password, **extra_fields)

    def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
        if backend is None:
            backends = get_backends()
            if len(backends) == 1:
                backend = backends[0]
            else:
                raise ImproperlyConfigured(
                    "설정된 인증 backend가 여러 개이므로 `backend` 인자를 명시해야 합니다."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend는 문자열 경로여야 합니다 (예: 'django.contrib.auth.backends.ModelBackend')"
            )

        backend = load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()


class User(AbstractBaseUser, PermissionsMixin):
    class SocialType(models.TextChoices):
        EMAIL = "email", "Email"
        KAKAO = "kakao", "Kakao"
        GOOGLE = "google", "Google"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=30)
    profile_image = models.CharField(max_length=500, blank=True, null=True)
    social_type = models.CharField(
        max_length=20, choices=SocialType.choices, default=SocialType.EMAIL
    )
    social_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("user")
