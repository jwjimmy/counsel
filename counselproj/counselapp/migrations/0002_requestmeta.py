# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-08 20:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counselapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('server_software', models.CharField(max_length=1000)),
                ('http_origin', models.CharField(max_length=1000)),
                ('server_protocol', models.CharField(max_length=1000)),
                ('systemroot', models.CharField(max_length=1000)),
                ('virtual_env', models.CharField(max_length=1000)),
                ('java_home', models.CharField(max_length=1000)),
                ('path', models.CharField(max_length=1000)),
                ('http_cookie', models.CharField(max_length=1000)),
                ('computername', models.CharField(max_length=1000)),
                ('userdomain', models.CharField(max_length=1000)),
                ('http_referer', models.CharField(max_length=1000)),
                ('remote_addr', models.CharField(max_length=1000)),
            ],
        ),
    ]
