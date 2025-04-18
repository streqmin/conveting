import os
import uuid
from django.db import models
from django.conf import settings


def dog_photo_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    unique_id = uuid.uuid4().hex[:8]
    user_id = str(instance.user.id)
    dog_name = instance.name.replace(" ", "_")  # 공백 제거
    new_filename = f"{user_id}_{dog_name}_{unique_id}.{ext}"
    return os.path.join("dog_photos", new_filename)


class Dog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dogs"
    )
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to=dog_photo_upload_path)
    birth_date = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    BREED_CHOICES = [
        ("골든 리트리버", "골든 리트리버"),
        ("래브라도 리트리버", "래브라도 리트리버"),
        ("푸들", "푸들"),
        ("포메라니안", "포메라니안"),
        ("말티즈", "말티즈"),
        ("시추", "시추"),
        ("요크셔 테리어", "요크셔 테리어"),
        ("비숑 프리제", "비숑 프리제"),
        ("웰시 코기", "웰시 코기"),
        ("프렌치 불도그", "프렌치 불도그"),
        ("치와와", "치와와"),
        ("미니어처 핀셔", "미니어처 핀셔"),
        ("미니어처 슈나우저", "미니어처 슈나우저"),
        ("시바 이누", "시바 이누"),
        ("닥스훈트", "닥스훈트"),
        ("보더 콜리", "보더 콜리"),
        ("저먼 셰퍼드", "저먼 셰퍼드"),
        ("도베르만", "도베르만"),
        ("잭 러셀 테리어", "잭 러셀 테리어"),
        ("시베리안 허스키", "시베리안 허스키"),
        ("기타", "기타"),
    ]

    breed = models.CharField(max_length=100, choices=BREED_CHOICES)
    weight = models.FloatField(null=True, blank=True)
    neutered = models.BooleanField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "강아지"
        verbose_name_plural = "강아지"
