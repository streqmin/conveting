from django.db import models
from django.conf import settings
from dogs.models import Dog
from prediction.models import DiseaseInfo, Prediction

from django.utils import timezone


def post_image_upload_path(instance, filename):
    user_id = instance.user.id
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    return f"posts/{user_id}/{timestamp}-{filename}"


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="작성자",
    )
    dog = models.ForeignKey(
        Dog,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="반려견",
    )
    title = models.CharField("제목", max_length=200)
    content = models.TextField("내용")
    image = models.ImageField("이미지", upload_to=post_image_upload_path, null=True, blank=True)

    # breed는 dog에서 자동 설정됨
    breed = models.CharField(
        max_length=50, choices=Dog.BREED_CHOICES, null=True, blank=True, verbose_name="견종"
    )

    disease = models.ForeignKey(
        DiseaseInfo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="질환"
    )
    body_part = models.CharField(
        max_length=10,
        choices=Prediction.BodyPart.choices,
        null=True,
        blank=True,
        verbose_name="질환 부위",
    )

    created_at = models.DateTimeField("작성 시각", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시각", auto_now=True)

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글"

    def save(self, *args, **kwargs):
        if self.dog and self.dog.breed:
            self.breed = self.dog.breed
        super().save(*args, **kwargs)
