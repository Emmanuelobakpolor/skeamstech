from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
)
from .models import ShopTab, ShopCategory, ShopProduct


class ShopProductSerializer(ModelSerializer):
    image_url = SerializerMethodField()
    specs = SerializerMethodField()
    category_name = CharField(source='category.name', read_only=True)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def get_specs(self, obj):
        specs = {}
        if obj.spec_speed:
            specs['speed'] = obj.spec_speed
        if obj.spec_weight:
            specs['weight'] = obj.spec_weight
        if obj.spec_voltage:
            specs['voltage'] = obj.spec_voltage
        if obj.spec_power:
            specs['power'] = obj.spec_power
        if obj.spec_storage:
            specs['storage'] = obj.spec_storage
        if obj.spec_connectivity:
            specs['connectivity'] = obj.spec_connectivity
        return specs

    class Meta:
        model = ShopProduct
        fields = [
            'id',
            'name',
            'description',
            'application',
            'image_url',
            'specs',
            'category_name',
        ]


class ShopCategorySerializer(ModelSerializer):
    products = ShopProductSerializer(many=True, read_only=True)

    class Meta:
        model = ShopCategory
        fields = ['id', 'name', 'subtitle', 'products']


class ShopTabSerializer(ModelSerializer):
    categories = ShopCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ShopTab
        fields = ['id', 'name', 'display_name', 'description', 'order', 'is_hardcoded', 'categories']
