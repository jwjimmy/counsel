# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counselapp', '0006_auto_20170207_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='estate',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='visit',
            name='visitor',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
