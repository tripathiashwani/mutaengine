# Generated by Django 5.0.2 on 2024-11-07 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_remove_smtp_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='smtp',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
