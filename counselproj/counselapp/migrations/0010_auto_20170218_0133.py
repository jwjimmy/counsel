# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 06:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('counselapp', '0009_delete_requestmeta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visit',
            old_name='estate',
            new_name='url',
        ),
    ]
