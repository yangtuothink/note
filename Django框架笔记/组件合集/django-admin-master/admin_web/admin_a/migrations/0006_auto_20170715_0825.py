# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-07-15 00:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_a', '0005_auto_20170714_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ip_host',
            options={'verbose_name_plural': 'ip地址表'},
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='role',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_a.Direction', verbose_name='角色'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='tags',
            field=models.ManyToManyField(to='admin_a.IP_host', verbose_name='主机'),
        ),
    ]
