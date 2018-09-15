from rest_framework import serializers

from .models import ShoppingCart, OrderInfo, OrderGoods

class ShoppingCartSerializer(serializers.ModelSerializer):
    """
        购物车
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = ShoppingCart
        fields = ('user', 'goods', 'nums', 'add_time')

class OrderInfoSerializer(serializers.ModelSerializer):
    """
        订单信息
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = OrderInfo
        fields = ('id', 'user',
                  'order_sn', 'trade_no', 'pay_status', 'post_script', 'order_mount', 'pay_time',
                  'address', 'signer_name', 'signer_phone',
                  'add_time', 'status')

class OrderGoodsSerializer(serializers.ModelSerializer):
    """
        订单商品
    """
    class Meta:
        model = OrderGoods
        fields = ('id', 'order', 'goods', 'nums', 'add_time', 'status')