from django.shortcuts import render

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import UserFavSerializer, UserDetailSerilizer, UserLeavingMessageSerializer, UserAddrSerializer
from .models import UserFav, UserLeavingMessage, UserAddress
from extrac.utils.REST.Permissions import IsOwnerOrReadOnly
# Create your views here.
class UserFavViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        用户收藏
    retrieve:
        获取用户某个收藏
    create:
        创建收藏
    destroy:
        取消收藏
    """
    serializer_class = UserFavSerializer
    queryset = UserFav.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    lookup_field = 'goods_id' # 调整 id 的 source

    def perform_create(self, serializer):
        instance = serializer.save()
        goods = instance.goods
        goods.fav_num += 1
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.fav_num -= 1
        goods.save()
        instance.delete()

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'destroy':
            return UserFavSerializer
        return UserDetailSerilizer

class UserLeavingMessageViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """
        用户留言
    """
    serializer_class = UserLeavingMessageSerializer
    queryset = UserLeavingMessage.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

class UserAddrViewSet(viewsets.ModelViewSet):
    """
        用户收货地址
    """
    serializer_class = UserAddrSerializer
    queryset = UserAddress.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)