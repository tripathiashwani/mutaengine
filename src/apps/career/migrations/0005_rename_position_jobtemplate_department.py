# Generated by Django 5.1.2 on 2024-10-17 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("career", "0004_alter_jobtemplate_slug"),
    ]

    operations = [
        migrations.RenameField(
            model_name="jobtemplate",
            old_name="position",
            new_name="department",
        ),
    ]