from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
)
from .models import ShopTab, ShopCategory, ShopProduct, ProductImage, ProductModel, ProductModelImage


# Public read-only serializers for product images
class ProductImageSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url', 'order']


class ProductModelImageSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url

    class Meta:
        model = ProductModelImage
        fields = ['id', 'image_url', 'order']


class ProductModelSerializer(ModelSerializer):
    images = ProductModelImageSerializer(many=True, read_only=True)
    specs = SerializerMethodField()

    def get_specs(self, obj):
        specs = {}
        for key in ['speed', 'weight', 'voltage', 'power', 'storage', 'connectivity']:
            val = getattr(obj, f'spec_{key}', '')
            if val:
                specs[key] = val
        return specs

    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'specs', 'images', 'order']


class ShopProductSerializer(ModelSerializer):
    image_url = SerializerMethodField()
    specs = SerializerMethodField()
    category_name = CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    product_models = ProductModelSerializer(many=True, read_only=True)

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
            'images',
            'product_models',
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


# ============================================================================
# ADMIN SERIALIZERS (for write operations)
# ============================================================================


class AdminProductImageSerializer(ModelSerializer):
    """Writable serializer for product images"""
    image_url = SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'order', 'created_at']
        read_only_fields = ['id', 'image_url', 'created_at']
        extra_kwargs = {'image': {'required': True, 'write_only': True}}


class AdminProductModelImageSerializer(ModelSerializer):
    """Writable serializer for product model images"""
    image_url = SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.image.url) if request else obj.image.url

    class Meta:
        model = ProductModelImage
        fields = ['id', 'image', 'image_url', 'order', 'created_at']
        read_only_fields = ['id', 'image_url', 'created_at']
        extra_kwargs = {'image': {'required': True, 'write_only': True}}


class AdminProductModelSerializer(ModelSerializer):
    """Writable serializer for product models"""
    images = AdminProductModelImageSerializer(many=True, read_only=True)

    class Meta:
        model = ProductModel
        fields = [
            'id',
            'name',
            'spec_speed',
            'spec_weight',
            'spec_voltage',
            'spec_power',
            'spec_storage',
            'spec_connectivity',
            'order',
            'created_at',
            'images',
        ]
        read_only_fields = ['id', 'created_at', 'images']


class AdminShopTabSerializer(ModelSerializer):
    """Writable serializer for admin operations on ShopTab"""

    class Meta:
        model = ShopTab
        fields = [
            'id',
            'name',
            'display_name',
            'description',
            'order',
            'is_active',
            'is_hardcoded',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class AdminShopCategorySerializer(ModelSerializer):
    """Writable serializer for admin operations on ShopCategory"""

    tab_name = CharField(source='tab.display_name', read_only=True)

    class Meta:
        model = ShopCategory
        fields = [
            'id',
            'tab',
            'tab_name',
            'name',
            'subtitle',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'tab_name', 'created_at']


class AdminShopProductSerializer(ModelSerializer):
    """Writable serializer for admin operations on ShopProduct with image upload"""

    image_url = SerializerMethodField()
    category_name = CharField(source='category.name', read_only=True)
    images = AdminProductImageSerializer(many=True, read_only=True)
    product_models = AdminProductModelSerializer(many=True, read_only=True)

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    class Meta:
        model = ShopProduct
        fields = [
            'id',
            'category',
            'category_name',
            'name',
            'description',
            'application',
            'image',
            'image_url',
            'images',
            'product_models',
            'spec_speed',
            'spec_weight',
            'spec_voltage',
            'spec_power',
            'spec_storage',
            'spec_connectivity',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['id', 'category_name', 'image_url', 'images', 'product_models', 'created_at']
        extra_kwargs = {
            'image': {
                'required': False,
                'allow_null': True,
                'write_only': True,
            }
        }
