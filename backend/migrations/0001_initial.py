# Generated by Django 3.1.7 on 2021-03-09 15:20

import backend.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator(), backend.models.User.validate_edu_email])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('university', models.CharField(max_length=50)),
                ('thumbs_up', models.PositiveIntegerField(default=0)),
                ('thumbs_down', models.PositiveIntegerField(default=0)),
                ('bio', models.CharField(max_length=5000, null=True)),
                ('classification', models.CharField(max_length=50, null=True, validators=[backend.models.User.validate_classification])),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('negotiable', models.BooleanField()),
                ('condition', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=5000, null=True)),
                ('location', models.CharField(max_length=50)),
                ('date_created', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.user')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(unique=True)),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='backend.listing')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.listing')),
            ],
        ),
    ]
