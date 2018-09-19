
from django.db.models import Q

from rest_framework import serializers

from .models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd

class GoodImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ('image', )

class GoodsCategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsCategorySerializer2(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'

class GoodsCategorySerializer(serializers.ModelSerializer):
    sub_cat = GoodsCategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'
        depth = 0

class GoodsSerializer(serializers.ModelSerializer):
    category = GoodsCategorySerializer()
    images = GoodImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'

class BrandsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'

class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandsSerializer(many=True)

    goods = serializers.SerializerMethodField()
    def get_goods(self, obj):
        value = obj.id
        all_goods = Goods.objects.filter(Q(category_id=value) |
                                   Q(category__parent_category_id=value) |
                                   Q(category__parent_category__parent_category_id=value))
        goods_ser = GoodsSerializer(all_goods, many=True)
        return goods_ser.data

    sub_cat = GoodsCategorySerializer2(many=True)

    ad_goods = serializers.SerializerMethodField()
    def get_ad_goods(self, obj):
        ret = {}
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category__id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(goods_ins, many=False).data
        ret['id'] = goods_json.get('id', None)
        ret['goods_front_image'] = goods_json.get('goods_front_image', None)
        print('context =', self.context)
        return ret

    class Meta:
        model = GoodsCategory
        fields = '__all__'