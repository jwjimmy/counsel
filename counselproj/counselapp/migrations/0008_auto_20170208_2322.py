# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-09 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counselapp', '0007_auto_20170208_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='estate',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='visit',
            name='visitor',
            field=models.CharField(default='', max_length=2000),
        ),
    ]