# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-08 11:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_a', '0003_userinfo_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='gender',
            field=models.CharField(choices=[('M', '西山'), ('F', '北理工')], default='F', max_length=4, verbose_name='位置'),
        ),
    ]
