# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-15 21:05
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_auto_20180914_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userfav',
            name='goods',
            field=models.ForeignKey(help_text='商品的id', on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='userleavingmessage',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='userleavingmessage',
            name='subject',
            field=models.CharField(default='', help_text='留言主题', max_length=100, verbose_name='主题'),
        ),
        migrations.AlterField(
            model_name='userleavingmessage',
            name='user',
            field=models.ForeignKey(help_text='所属用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
    ]
