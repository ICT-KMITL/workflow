# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-22 20:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflows', '0010_auto_20170519_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimerEventBased',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('eventTime', models.DateField(default=django.utils.timezone.now)),
                ('currentFlow', models.CharField(default='', max_length=50)),
                ('elementId', models.CharField(default='', max_length=50)),
                ('assignToUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timerAssignUser', to=settings.AUTH_USER_MODEL)),
                ('belongToWFId', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workflows.ExecutingFlow')),
            ],
        ),
        migrations.AlterField(
            model_name='pendingtask',
            name='taskName',
            field=models.CharField(max_length=100),
        ),
    ]