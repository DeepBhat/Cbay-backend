# Generated by Django 3.1.7 on 2021-04-15 11:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20210403_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 15, 6, 54, 37, 136822)),
        ),
    ]