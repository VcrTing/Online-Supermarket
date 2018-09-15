
import django_filters
from django.db.models import Q
from django_filters import rest_framework as filters

from .models import Goods

class GoodsFilter(filters.FilterSet):
    """
    过滤器 - 商品
    """
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text='最低价格')
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte', help_text='最高价格')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', help_text="商品名称")

    top_category = django_filters.NumberFilter(method='top_category_filter', help_text="")

    def top_category_filter(self, queryset, name, value):
        queryset = queryset.filter(Q(category_id=value) |
                                   Q(category__parent_category_id=value) |
                                   Q(category__parent_category__parent_category_id=value))
        return queryset

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot']