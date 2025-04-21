from django.db import models
from prediction.models import DiseaseInfo, Prediction
from dogs.models import Dog


from django.db import models
from django.conf import settings
from dogs.models import Dog  # dog 모델 위치에 맞게 import 경로 조정


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
    category = models.ForeignKey(
        "PostCategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
        verbose_name="카테고리",
    )

    title = models.CharField("제목", max_length=200)
    content = models.TextField("내용")
    image = models.CharField("이미지 경로", max_length=500, null=True, blank=True)

    created_at = models.DateTimeField("작성 시각", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시각", auto_now=True)

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글"

    def __str__(self):
        return f"{self.title} - {self.user}"


class PostCategory(models.Model):
    breed = models.CharField(
        max_length=50, choices=Dog.BREED_CHOICES, null=True, blank=True, verbose_name="견종"
    )

    disease = models.ForeignKey(
        DiseaseInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="post_categories",
        verbose_name="질환",
    )

    body_part = models.CharField(
        max_length=10,
        choices=Prediction.BodyPart.choices,
        null=True,
        blank=True,
        verbose_name="질환 부위",
    )

    class Meta:
        verbose_name = "게시글 카테고리"
        verbose_name_plural = "게시글 카테고리"

    def __str__(self):
        parts = []
        if self.breed:
            parts.append(self.breed)
        if self.disease:
            parts.append(self.disease.name)
        if self.body_part:
            parts.append(dict(Prediction.BodyPart.choices).get(self.body_part, self.body_part))
        return " / ".join(parts) or "카테고리 없음"
