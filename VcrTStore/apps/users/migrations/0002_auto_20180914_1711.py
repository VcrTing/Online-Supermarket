# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-14 17:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='password',
            field=models.CharField(max_length=120, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='电话'),
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='add_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='添加时间'),
        ),
    ]
