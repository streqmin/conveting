# Generated by Django 5.1.1 on 2025-04-21 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prediction", "0009_alter_prediction_request_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="prediction",
            name="request_id",
            field=models.CharField(max_length=36, verbose_name="예측 요청 ID"),
        ),
    ]
