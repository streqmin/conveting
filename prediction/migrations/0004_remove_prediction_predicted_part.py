# Generated by Django 5.1.1 on 2025-04-20 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("prediction", "0003_prediction"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="prediction",
            name="predicted_part",
        ),
    ]
