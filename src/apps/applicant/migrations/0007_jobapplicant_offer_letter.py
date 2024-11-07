# Generated by Django 5.0.2 on 2024-10-30 16:36

import src.apps.common.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applicant", "0006_alter_jobapplicant_resume"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplicant",
            name="offer_letter",
            field=models.FileField(
                blank=True, null=True, upload_to=src.apps.common.utils.get_upload_folder
            ),
        ),
    ]