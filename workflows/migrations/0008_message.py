# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-02 18:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflows', '0007_channel_channeljoin_pendingtask'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('msg', models.TextField(max_length=200)),
                ('timestamp', models.TimeField()),
                ('receiver', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('room', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='workflows.Channel')),
                ('sender', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]