# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-09-10 15:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(default=0, verbose_name='商品数量')),
                ('add_time', models.DateField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
                ('status', models.NullBooleanField(default=True, help_text='数据状态', verbose_name='数据状态')),
            ],
            options={
                'verbose_name': '订单and商品',
                'verbose_name_plural': '订单and商品',
            },
        ),
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.CharField(max_length=50, unique=True, verbose_name='订单编号')),
                ('trade_no', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='随机号')),
                ('pay_status', models.CharField(choices=[('success', '成功'), ('cancle', '取消'), ('waitpay', '待支付')], max_length=10, verbose_name='支付状态')),
                ('post_script', models.CharField(max_length=11, verbose_name='订单留言')),
                ('order_mount', models.FloatField(default=0.0, verbose_name='订单金额')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='支付时间')),
                ('address', models.CharField(default='', max_length=100, verbose_name='收货地址')),
                ('signer_name', models.CharField(default='', max_length=20, verbose_name='签收人')),
                ('signer_phone', models.CharField(max_length=11, verbose_name='联系电话')),
                ('add_time', models.DateField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
                ('status', models.NullBooleanField(default=True, help_text='数据状态', verbose_name='数据状态')),
            ],
            options={
                'verbose_name': '订单信息',
                'verbose_name_plural': '订单信息',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField(default=0)),
                ('add_time', models.DateField(default=datetime.datetime.now, help_text='添加时间', verbose_name='添加时间')),
                ('status', models.NullBooleanField(default=True, help_text='数据状态', verbose_name='数据状态')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods')),
            ],
            options={
                'verbose_name': '购物车',
                'verbose_name_plural': '购物车',
            },
        ),
    ]
