# Generated by Django 5.1.2 on 2024-10-24 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applicant", "0004_alter_jobapplicant_manager"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobapplicant",
            name="joining_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
