from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from apps.goods.models import Goods

User = get_user_model()
# Create your models here.

class UserFav(models.Model):
    """
    用户收藏
    """
    user = models.ForeignKey(User, verbose_name='用户')
    goods = models.ForeignKey(Goods, verbose_name='商品', help_text='商品的id')

    add_time = models.DateField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')
    status = models.NullBooleanField(default=True, verbose_name='数据状态', help_text='数据状态')

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')

    def __str__(self):
        return self.user.username

class UserLeavingMessage(models.Model):
    """
    用户留言
    """
    MESSAGE_CHOICES = (
        (1, '留言'),
        (2, '投诉'),
        (3, '询问'),
        (4, '售后'),
        (5, '求购')
    )
    user = models.ForeignKey(User, verbose_name='用户', help_text='所属用户')
    message_type = models.SmallIntegerField(default=1, choices=MESSAGE_CHOICES, verbose_name='用户留言',
                                            help_text=u'留言类型：1（留言），2（投诉），3（询问），4（售后）')
    subject = models.CharField(max_length=100, verbose_name='主题', default='', help_text='留言主题')
    message = models.TextField(default='', verbose_name='留言内容', help_text='留言内容')
    file = models.FileField(upload_to='message/files', help_text='上传的文件')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')
    status = models.NullBooleanField(default=True, verbose_name='数据状态', help_text='数据状态')

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message

class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name='用户')
    province = models.CharField(max_length=100, default='', verbose_name='省')
    city = models.CharField(max_length=100, default='', verbose_name='市')
    area = models.CharField(max_length=100, default='', verbose_name='区')
    address = models.CharField(max_length=100, default='', verbose_name='详细地址')
    signer_name = models.CharField(max_length=100, default='', verbose_name='签收人')
    signer_phone = models.CharField(max_length=11, default='', verbose_name='签收人电话')

    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', help_text='添加时间')
    status = models.NullBooleanField(default=True, verbose_name='数据状态', help_text='数据状态')

    class Meta:
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address