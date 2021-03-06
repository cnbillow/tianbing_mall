from django.shortcuts import render

# Create your views here.
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView


# GET /categories/(?P<category_id>\d+)/skus?page=xxx&page_size=xxx&ordering=xxx
from goods import serializers
from goods.models import SKU
from goods.serializers import SKUSerializer

# docker run -dti --network=host --name=elasticsearch -v /home/python/elasticsearch-2.4.6/config:/usr/share/elasticsearch/config delron/elasticsearch-ik:2.4.6-1.0
# 创建容器注意点:1,-v 映射配置文件夹;2,只要不是最新的版本需要指定版本


class SKUListView(ListAPIView):
    """
    SKU商品列表视图:
            对商品数据进行[分页],并[排序]:create(默认),price,sales
    :return:1,序列器实现:"id", "name", "price", "default_image_url", "comments"
            2,分页时django默认返回:count	next previous results
    """
    serializer_class = SKUSerializer

    # 指定后端过滤器:使用DRF提供的OrderingFilter过滤器
    filter_backends = (OrderingFilter,)
    # 使用OrderFilter则需指明ordering_fields属性可进行排序的字段
    ordering_fields = ("create", "price", "sales")

    def get_queryset(self):
        """分配get_object()方法使用的查询对象"""
        category_id = self.kwargs["category_id"]
        # category是一个外键,数据表存的是category_id;is_lanched?
        return SKU.objects.filter(category_id=category_id, is_launched=True)


class SKUSearchViewSet(HaystackViewSet):
    """
    sku搜索:
        返回搜索结果的列表数据:使用默认的全局分页
    继承:
        haystack提供的HaystackViewSet,来操作索引类
    """

    index_models = [SKU]
    serializer_class = serializers.SKUIndexSerializer






































