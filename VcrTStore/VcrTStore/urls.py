"""VcrTStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin

from django.views.static import serve
from django.views.generic import TemplateView

from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from apps.goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, IndexCategoryViewSet
from apps.users.views import SmsCodeViewSet, UserRegViewSet
from apps.operation.views import UserFavViewSet, UserLeavingMessageViewSet, UserAddrViewSet
from apps.trade.views import ShoppingCartViewSet, OrderInfoViewSet, OrderGoodsViewSet, AlipayView

from VcrTStore.settings import MEDIA_ROOT

router = DefaultRouter()

# goods
router.register(r'goods', GoodsListViewSet, base_name='goods')
router.register(r'categorys', CategoryViewSet, base_name='categorys')
router.register(r'banners', BannerViewSet, base_name='banners')
router.register(r'indexgoods', IndexCategoryViewSet, base_name='indexgoods')

# users
router.register(r'code', SmsCodeViewSet, base_name='code')
router.register(r'users', UserRegViewSet, base_name='users')

# operation
router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
router.register(r'messages', UserLeavingMessageViewSet, base_name='messages')
router.register(r'address', UserAddrViewSet, base_name='address')

# trade
router.register(r'shopcarts', ShoppingCartViewSet , base_name='shopcarts')
router.register(r'orders', OrderInfoViewSet , base_name='orders')
router.register(r'ordergoods', OrderGoodsViewSet , base_name='ordergoods')

# goods_set = GoodsListViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),

    url(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # url(r'^api-token-auth/', views.obtain_auth_token), drf自带的token认证
    url(r'^login/$', obtain_jwt_token), # jwt认证接口

    url(r'^docs/', include_docs_urls(title='VcrT超市')),

    url(r'^index/', TemplateView.as_view(template_name='index.html'), name='index'),

    # 商品列表
    url(r'^', include(router.urls)),
    # url(r'^goods/$', GoodsListView.as_view(), name='good_list'),
    # url(r'^goods/$', goods_set, name='good_list'),

    # 支付
    url(r'^alipay/return', AlipayView.as_view(), name='alipay'),

    # social 认证
    url('', include('social_django.urls', namespace='social')),
]
