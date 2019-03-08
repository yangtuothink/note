# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-04 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32, verbose_name='用户名')),
                ('passwd', models.CharField(max_length=32, verbose_name='密码')),
            ],
            options={
                'verbose_name_plural': '方向（视频方向）',
            },
        ),
    ]
