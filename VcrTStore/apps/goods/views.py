
from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.authentication import TokenAuthentication

from rest_framework_extensions.cache.mixins import CacheResponseMixin

from django_filters.rest_framework.backends import DjangoFilterBackend

from .models import Goods, GoodsCategory, Banner
from .serializers import GoodsSerializer, GoodsCategorySerializer, BannerSerializer, IndexCategorySerializer
from .filters import GoodsFilter
from extrac.utils.REST.Pager import LimitOffsetPager, PageNumberPager

# Create your views here.
class GoodsListViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品列表页, 分页，过滤，搜索，排序
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = PageNumberPager
    authentication_classes = (TokenAuthentication, )

    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief', 'goods_desc')
    ordering_fields = ('sold_num', 'shop_price')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    商品分类列表数据
    """
    queryset = GoodsCategory.objects.filter(category_type = 1)
    serializer_class = GoodsCategorySerializer
    pagination_class = None

class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        轮播图
    """
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        商品分类
    """
    queryset = GoodsCategory.objects.filter(is_tab=True, name__in=['生鲜食品', '	酒水饮料', '粮油副食'])
    serializer_class = IndexCategorySerializer

"""
第一个版本
class GoodsListView(APIView):
    # 查询所有的商品
    def get(self, request, format=None):
        print('进来了')
        goods = Goods.objects.all()
        goods_ser = GoodsSerializer(goods, many=True)
        return Response(goods_ser.data)

    def post(self, request, format=None):
        ser = GoodsSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
class GoodsListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = LimitOffsetPager

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

"""