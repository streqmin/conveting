from django.db import models


class DiseaseInfo(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "질환 정보"
        verbose_name_plural = "질환 정보"
