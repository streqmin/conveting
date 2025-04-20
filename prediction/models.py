from django.db import models


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
