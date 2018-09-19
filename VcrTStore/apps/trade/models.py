from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.goods.models import Goods

User = get_user_model()
# Create your models here.

class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User)
    goods = models.ForeignKey(Goods)
    nums = models.IntegerField(default=0, verbose_name='购物车数量')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')
    status = models.NullBooleanField(default=True, verbose_name='数据状态', help_text='数据状态')

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')

    def __str__(self):
        return '%s(%d)'.format(self.goods.name, self.nums)

class OrderInfo(models.Model):
    """
    订单信息
    """
    ORDER_STATUS = (
        ('TRADE_SUCCESS', '成功'),
        ('TRADE_CLOSED', '超时关闭'),
        ('WAIT_BUYER_PAY', '交易创建'),
        ('TRADE_FINISHED', '交易结束'),
        ('paying', '待支付')
    )
    PAY_STATUS = (
        ('alipay', '支付宝'),
        ('wechat', '微信')
    )
    user = models.ForeignKey(User, verbose_name=u'用户')
    order_sn = models.CharField(max_length=50, null=False, blank=True, unique=True, verbose_name='订单编号')
    trade_no = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name=u'随机号')
    pay_status = models.CharField(choices=ORDER_STATUS, default='paying', max_length=30, verbose_name='支付状态')
    post_script = models.CharField(max_length=11, verbose_name='订单留言')
    order_mount = models.FloatField(default=0.0, verbose_name='订单金额')
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name='支付时间')

    # 用户信息
    address = models.CharField(max_length=100, default='', verbose_name='收货地址')
    signer_name = models.CharField(max_length=20, default='', verbose_name='签收人')
    signer_phone = models.CharField(max_length=11, verbose_name='联系电话')

    add_time = models.DateTimeField(default=timezone.now, verbose_name='添加时间', help_text='添加时间')
    status = models.NullBooleanField(default=True, verbose_name='数据状态', help_text='数据状态')

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn

class OrderGoods(models.Model):
    """
    订单的商品详情
    """
    user = models.ForeignKey(User, validators='用户', null=True)
    order = models.ForeignKey(OrderInfo, verbose_name='商品', related_name='goods')
    goods = models.ForeignKey(Goods, verbose_name='商品数量')
    nums = models.IntegerField(default=0, verbose_name='商品数量')

    add_time = models.DateField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')
    status = models.NullBooleanField(default=True, verbose_name='数据状态', help_text='数据状态')

    class Meta:
        verbose_name = '订单and商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name + self.order.trade_no