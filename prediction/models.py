from django.db import models
from django.conf import settings
from dogs.models import Dog


class DiseaseInfo(models.Model):
    # 예: "papule_plaque"·"scale_collarette" … API에서 키 값으로 쓰기 좋습니다.
    code = models.SlugField(
        max_length=40,
        unique=True,
        help_text="영문 식별자(예: papule_plaque)",
    )

    # 한국어 질환명(모델이 예측 결과로 사용자에게 보여줄 이름)
    name = models.CharField("질환명(한글)", max_length=100)

    # ────────── 상세 정보 ──────────
    symptoms = models.TextField("주요 증상", max_length=1000)
    home_care = models.TextField("1차 대처(가정)", max_length=1000)
    vet_care = models.TextField("수의학적 진단·치료", max_length=1200)

    # 자동 시간 기록
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "질환 정보"
        verbose_name_plural = "질환 정보"

    def __str__(self):
        return self.name


def prediction_image_path(instance, filename):
    instance_id = instance.id
    user_id = instance.user_id
    dog_id = instance.dog_id
    return f"predictions/{user_id}/{dog_id}/{instance_id}/{filename}"


class Prediction(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="사용자",
    )
    dog = models.ForeignKey(
        Dog,
        on_delete=models.CASCADE,
        verbose_name="반려견",
    )

    # 업로드한 원본 이미지
    image = models.ImageField(
        upload_to=prediction_image_path,
        max_length=500,
        verbose_name="질환 사진",
    )

    predicted_part = models.CharField("예측 부위", max_length=50)
    predicted_disease = models.CharField("예측 질환", max_length=100)

    probability = models.FloatField("예측 확률")
    is_normal = models.BooleanField("정상 여부", default=False)

    created_at = models.DateTimeField("생성 시각", auto_now_add=True)

    class Meta:
        verbose_name = "예측 결과"
        verbose_name_plural = "예측 결과"
