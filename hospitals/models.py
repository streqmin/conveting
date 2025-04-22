from django.db import models


class AnimalHospital(models.Model):
    name = models.CharField("병원명", max_length=200)
    phone = models.CharField("전화번호", max_length=50, blank=True)
    raw_address = models.CharField("소재지", max_length=200)
    license_no = models.CharField("인허가번호", max_length=50)
    full_address = models.CharField("상세주소", max_length=300, blank=True)
    latitude = models.FloatField("위도", null=True, blank=True)
    longitude = models.FloatField("경도", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "동물병원"
        verbose_name_plural = "동물병원 목록"
