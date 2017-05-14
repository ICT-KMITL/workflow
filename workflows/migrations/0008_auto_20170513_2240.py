# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 22:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workflows', '0007_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ChannelJoin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('channelId', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='workflows.Channel')),
                ('userId', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExecutingFlow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PendingTask',
            fields=[
                ('taskId', models.AutoField(primary_key=True, serialize=False)),
                ('assignToUser', models.TextField(max_length=50)),
                ('form', models.TextField(max_length=400)),
                ('taskName', models.TextField(max_length=100)),
                ('State', models.BooleanField(default=True)),
                ('listenner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='message',
            name='msg',
            field=models.TextField(max_length=200),
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='workflows.Channel'),
        ),
    ]
