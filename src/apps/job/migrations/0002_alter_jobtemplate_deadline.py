# Generated by Django 5.0.9 on 2024-10-27 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobtemplate',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
