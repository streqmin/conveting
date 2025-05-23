# Generated by Django 5.1.1 on 2025-04-20 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prediction", "0004_remove_prediction_predicted_part"),
    ]

    operations = [
        migrations.AddField(
            model_name="prediction",
            name="predicted_part",
            field=models.CharField(default="nothing", max_length=50, verbose_name="예측 부위"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="prediction",
            name="predicted_disease",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="predictions",
                to="prediction.diseaseinfo",
                verbose_name="예측 질환",
            ),
        ),
    ]
