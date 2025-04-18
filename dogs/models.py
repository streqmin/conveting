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
    breed = models.CharField(max_length=100)
    weight = models.FloatField(null=True, blank=True)
    neutered = models.BooleanField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "강아지"
        verbose_name_plural = "강아지"
