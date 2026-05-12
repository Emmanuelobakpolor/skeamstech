from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    CharField,
)

from .models import ShopTab, ShopCategory, ShopProduct, ProductImage


# ============================================================================
# HELPER FUNCTION
# ============================================================================

def build_image_url(serializer, image_field):
    """
    Safely build image URLs for both:
    - Cloudinary (absolute URLs)
    - Local Django media files (relative URLs)
    """

    if not image_field:
        return None

    image_url = image_field.url

    # Cloudinary/full URL
    if image_url.startswith("http"):
        return image_url

    # Local media URL
    request = serializer.context.get("request")
    return request.build_absolute_uri(image_url) if request else image_url


# ============================================================================
# PUBLIC SERIALIZERS
# ============================================================================

class ProductImageSerializer(ModelSerializer):
    image_url = SerializerMethodField()

    def get_image_url(self, obj):
        return build_image_url(self, obj.image)

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image_url",
            "order",
        ]


class ShopProductSerializer(ModelSerializer):
    image_url = SerializerMethodField()
    specs = SerializerMethodField()
    category_name = CharField(source="category.name", read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    def get_image_url(self, obj):
        # Use first gallery image if available, otherwise use hero image
        if obj.images.exists():
            return obj.images.first().image.url
        return build_image_url(self, obj.image)

    def get_specs(self, obj):
        spec_fields = [
            "speed",
            "weight",
            "voltage",
            "power",
            "storage",
            "connectivity",
        ]

        return {
            field: getattr(obj, f"spec_{field}")
            for field in spec_fields
            if getattr(obj, f"spec_{field}")
        }

    class Meta:
        model = ShopProduct
        fields = [
            "id",
            "name",
            "description",
            "application",
            "image_url",
            "images",
            "specs",
            "category_name",
        ]


class ShopCategorySerializer(ModelSerializer):
    products = ShopProductSerializer(many=True, read_only=True)

    class Meta:
        model = ShopCategory
        fields = [
            "id",
            "name",
            "subtitle",
            "products",
        ]


class ShopTabSerializer(ModelSerializer):
    categories = ShopCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ShopTab
        fields = [
            "id",
            "name",
            "display_name",
            "description",
            "order",
            "is_hardcoded",
            "categories",
        ]


# ============================================================================
# ADMIN SERIALIZERS
# ============================================================================

class AdminProductImageSerializer(ModelSerializer):
    """
    Writable serializer for product images
    """

    image_url = SerializerMethodField()

    def get_image_url(self, obj):
        return build_image_url(self, obj.image)

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "image_url",
            "order",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "image_url",
            "created_at",
        ]

        extra_kwargs = {
            "image": {
                "required": True,
                "write_only": True,
            }
        }


class AdminShopTabSerializer(ModelSerializer):
    """
    Writable serializer for admin operations on ShopTab
    """

    class Meta:
        model = ShopTab
        fields = [
            "id",
            "name",
            "display_name",
            "description",
            "order",
            "is_active",
            "is_hardcoded",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class AdminShopCategorySerializer(ModelSerializer):
    """
    Writable serializer for admin operations on ShopCategory
    """

    tab_name = CharField(source="tab.display_name", read_only=True)

    class Meta:
        model = ShopCategory
        fields = [
            "id",
            "tab",
            "tab_name",
            "name",
            "subtitle",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "tab_name",
            "created_at",
        ]


class AdminShopProductSerializer(ModelSerializer):
    """
    Writable serializer for admin operations on ShopProduct
    """

    image_url = SerializerMethodField()
    category_name = CharField(source="category.name", read_only=True)
    images = AdminProductImageSerializer(many=True, read_only=True)

    def get_image_url(self, obj):
        # Use first gallery image if available, otherwise use hero image
        if obj.images.exists():
            return obj.images.first().image.url
        return build_image_url(self, obj.image)

    class Meta:
        model = ShopProduct

        fields = [
            "id",
            "category",
            "category_name",
            "name",
            "description",
            "application",
            "image",
            "image_url",
            "images",
            "spec_speed",
            "spec_weight",
            "spec_voltage",
            "spec_power",
            "spec_storage",
            "spec_connectivity",
            "is_active",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "category_name",
            "image_url",
            "images",
            "created_at",
        ]

        extra_kwargs = {
            "image": {
                "required": False,
                "allow_null": True,
                "write_only": True,
            }
        }