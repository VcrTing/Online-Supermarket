
from rest_framework import serializers
from rest_framework import validators

from .models import UserFav, UserLeavingMessage, UserAddress
from apps.goods.serializers import GoodsSerializer

class UserDetailSerilizer(serializers.ModelSerializer):
    """
        用户收藏内容
    """
    goods = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ('goods',)

class UserFavSerializer(serializers.ModelSerializer):
    """
        用户收藏
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault() # 获取当前用户
    )
    class Meta:
        model = UserFav
        validators = [
            validators.UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message='已经收藏'
            )
        ]
        fields = ('goods', 'user', 'id')

class UserLeavingMessageSerializer(serializers.ModelSerializer):
    """
        用户留言
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    class Meta:
        model = UserLeavingMessage
        fields = ('id', 'user', 'message_type', 'subject', 'message', 'file', 'add_time')

class UserAddrSerializer(serializers.ModelSerializer):
    """
    用户收货地址
    """
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M')
    signer_mobile = serializers.CharField(source='signer_phone', help_text='接收者的电话')
    district = serializers.CharField(source='area', help_text='区')
    class Meta:
        model = UserAddress
        fields = ('id', 'user', 'province', 'city', 'district', 'address', 'signer_name', 'add_time', 'signer_mobile')