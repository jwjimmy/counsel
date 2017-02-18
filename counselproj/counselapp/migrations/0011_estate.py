# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 06:38
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('counselapp', '0010_auto_20170218_0133'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estate',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(default='', max_length=1000)),
                ('estate_type', models.IntegerField()),
            ],
        ),
    ]
