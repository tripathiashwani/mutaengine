# Generated by Django 5.0.2 on 2024-11-12 16:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0011_remove_offertemplate_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtemplate',
            name='joining_date',
            field=models.DateField(default=datetime.date(2024, 11, 20)),
        ),
    ]
