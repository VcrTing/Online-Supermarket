import time, datetime
import random

from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods
from apps.goods.models import Goods
from apps.goods.serializers import GoodsSerializer

from extrac.utils.PAY.alipay import AliPay
from VcrTStore.settings import ALIPAY

class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    """
        购物车
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField()
    goods = GoodsSerializer()
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShoppingCartSerializer(serializers.Serializer):
    """
        购物车
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True, min_value=1, label='商品数量', help_text='商品数量',
                                    error_messages={
                                        'required': '请选择购买数量',
                                        'min_value': '商品数量不能小于1',
                                    })
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all(), help_text='商品')

    def create(self, validated_data):
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']
        print('goods =', goods)
        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance
    # class Meta:
    #     model = ShoppingCart
    #     fields = ('user', 'goods', 'nums', 'add_time')


class OrderInfoSerializer(serializers.ModelSerializer):
    """
        订单信息
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    signer_mobile = serializers.CharField(source='signer_phone', help_text='收货人电话')

    alipay_url = serializers.SerializerMethodField(read_only=True)
    def get_alipay_url(self, obj):
        aplipay = AliPay(
            appid=ALIPAY['APPID'],
            app_notify_url=ALIPAY['NOTIFY_URL'],
            return_url=ALIPAY['RETURN_URL'],
            debug=ALIPAY['DEBUG'],
            app_private_key_path=ALIPAY['APP_PRIVATE_KEY'],
            alipay_public_key_path=ALIPAY['ALIPAY_PUBLIC_KEY']
        )
        url = aplipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount
        )
        ret_url = ALIPAY['ALIPAY_URL'] + '?{data}'.format(data = url)
        return ret_url

    def generate_order_sn(self):
        order_sn = '{time_str}{user_id}{ran_str}'.format(time_str=time.strftime('%Y%m%d%H%M'),
                                                         user_id=self.context['request'].user.id,
                                                         ran_str=random.randint(0, 1000))
        return order_sn
    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = ('id', 'user', 'add_time', 'alipay_url',
                  'order_sn', 'trade_no', 'pay_status', 'pay_time',
                  'post_script', 'order_mount', 'address', 'signer_name', 'signer_mobile')

class OrderDetailSerializer(serializers.ModelSerializer):
    """
        订单商品
    """
    goods = GoodsSerializer()

    alipay_url = serializers.SerializerMethodField(read_only=True)
    def get_alipay_url(self, obj):
        aplipay = AliPay(
            appid=ALIPAY['APPID'],
            app_notify_url=ALIPAY['NOTIFY_URL'],
            return_url=ALIPAY['RETURN_URL'],
            debug=ALIPAY['DEBUG'],
            app_private_key_path=ALIPAY['APP_PRIVATE_KEY'],
            alipay_public_key_path=ALIPAY['ALIPAY_PUBLIC_KEY']
        )
        url = aplipay.direct_pay(
            subject=obj.order_sn,
            out_trade_no=obj.order_sn,
            total_amount=obj.order_mount
        )
        ret_url = ALIPAY['ALIPAY_URL'] + '?{data}'.format(data = url)
        return ret_url
    class Meta:
        model = OrderGoods
        fields = '__all__'