# Generated by Django 5.0.2 on 2024-11-06 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("job", "0005_alter_jobtemplate_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobassignmenttemplate",
            name="objective",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]