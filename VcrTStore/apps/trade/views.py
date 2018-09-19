import time, datetime
import random
from django.shortcuts import render

from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from rest_framework import viewsets, mixins, views
from rest_framework import permissions
from rest_framework import authentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response

from extrac.utils.REST.Permissions import IsOwnerOrReadOnly

User = get_user_model()

from extrac.utils.PAY.alipay import AliPay
from VcrTStore.settings import ALIPAY
from .models import ShoppingCart, OrderInfo, OrderGoods
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer, OrderDetailSerializer
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
    lookup_field = 'goods_id'

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        return ShoppingCartSerializer

class OrderInfoViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
        订单信息
    """
    serializer_class = OrderInfoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        if self.action == 'retrieve':
            return OrderInfo.objects.filter(user=self.request.user)
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return OrderInfoSerializer
        return OrderInfoSerializer

    def generate_order_sn(self):
        order_sn = '{time_str}{user_id}{ran_str}'.format(time_str=time.strftime('%Y%m%d%H%M'),
                                                         user_id=self.request.user.id,
                                                         ran_str=random.randint(0, 1000))
        return order_sn

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for sc in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = sc.goods
            order_goods.nums = sc.nums
            order_goods.order = order
            order_goods.user = order.user
            order_goods.save()
            sc.delete()
        return order

class OrderGoodsViewSet(viewsets.ModelViewSet):
    # 订单商品
    serializer_class = OrderDetailSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_queryset(self):
        return OrderGoods.objects.filter(user=self.request.user)

class AlipayView(views.APIView):
    """
        阿里支付
    """
    def get(self, request):
        # deal return_url
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        aplipay = AliPay(
            appid=ALIPAY['APPID'],
            app_notify_url=ALIPAY['NOTIFY_URL'],
            return_url=ALIPAY['RETURN_URL'],
            debug=ALIPAY['DEBUG'],
            app_private_key_path=ALIPAY['APP_PRIVATE_KEY'],
            alipay_public_key_path=ALIPAY['ALIPAY_PUBLIC_KEY']
        )
        verify_ret = aplipay.verify(processed_dict, sign)

        if verify_ret is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', 'TRADE_SUCCESS')
            existed_orders = OrderInfo.objects.filter(order_sn = order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.datetime.now()
                existed_order.save()
            response = redirect('index')
            response.set_cookie('nextPath', 'pay', max_age=2)
            return response
        else:
            response = redirect('index')
            return response
    def post(self, request):
        # deal notify_url
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value
        sign = processed_dict.pop('sign', None)

        aplipay = AliPay(
            appid=ALIPAY['APPID'],
            app_notify_url=ALIPAY['NOTIFY_URL'],
            return_url=ALIPAY['RETURN_URL'],
            debug=ALIPAY['DEBUG'],
            app_private_key_path=ALIPAY['APP_PRIVATE_KEY'],
            alipay_public_key_path=ALIPAY['ALIPAY_PUBLIC_KEY']
        )
        verify_ret = aplipay.verify(processed_dict, sign)

        if verify_ret is True:
            order_sn = processed_dict.get('out_trade_no', None)
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)
            existed_orders = OrderInfo.objects.filter(order_sn = order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all()
                for order_good in order_goods:
                    goods = order_good.goods
                    goods.sold_num += 1
                    goods.save()
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.datetime.now()
                existed_order.save()
            return Response('success')
