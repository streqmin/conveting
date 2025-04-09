import uuid
from django.db import models

class User(models.Model):
    class SocialType(models.TextChoices):
        EMAIL = 'email', 'Email'
        KAKAO = 'kakao', 'Kakao'
        GOOGLE = 'google', 'Google'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    nickname = models.CharField(max_length=30)
    profile_image = models.CharField(max_length=500, blank=True, null=True)
    social_type = models.CharField(
        max_length=20,
        choices=SocialType.choices,
        default=SocialType.EMAIL
    )
    social_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nickname
