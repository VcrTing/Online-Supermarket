from django.shortcuts import render

from django.contrib.auth import get_user_model

from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from extrac.utils.REST.Permissions import IsOwnerOrReadOnly

User = get_user_model()

from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, OrderInfoSerializer, OrderGoodsSerializer
# Create your views here.
class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
        购物车
        List:
            获取购物车详情
        create:
            添加购物车
        retrieve:
            查看单条购物车
        update:
            更新
        destroy:
            删除单条购物车
        delete:
            清除购物记录
    """
    serializer_class = ShoppingCartSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

class OrderInfoViewSet(viewsets.ModelViewSet):
    """
        订单信息
    """
    serializer_class = OrderInfoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

class OrderGoodsViewSet(viewsets.ModelViewSet):
    """
        订单商品
    """
    serializer_class = OrderGoodsSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)