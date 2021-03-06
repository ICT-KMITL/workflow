# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 20:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentModel',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('dateOfBirth', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
    ]
