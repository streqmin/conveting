# Generated by Django 4.2.16 on 2025-04-10 05:09

import accounts.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "user", "verbose_name_plural": "users"},
        ),
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", accounts.models.UserManager()),
            ],
        ),
    ]
