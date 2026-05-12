from django.contrib import admin
from .models import ShopTab, ShopCategory, ShopProduct


class ShopProductInline(admin.TabularInline):
    model = ShopProduct
    extra = 1
    fields = [
        'name',
        'description',
        'application',
        'image',
        'spec_speed',
        'spec_weight',
        'spec_voltage',
        'spec_power',
        'spec_storage',
        'spec_connectivity',
        'is_active',
    ]


class ShopCategoryInline(admin.TabularInline):
    model = ShopCategory
    extra = 1
    fields = ['name', 'subtitle', 'is_active']


@admin.register(ShopTab)
class ShopTabAdmin(admin.ModelAdmin):
    list_display = ['id', 'display_name', 'name', 'order', 'is_hardcoded', 'is_active', 'created_at']
    list_filter = ['is_active', 'is_hardcoded']
    search_fields = ['display_name', 'name']
    readonly_fields = ['is_hardcoded']
    inlines = [ShopCategoryInline]
    fields = ['name', 'display_name', 'description', 'order', 'is_active', 'is_hardcoded']


@admin.register(ShopCategory)
class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'tab', 'subtitle', 'is_active', 'created_at']
    list_filter = ['is_active', 'tab']
    search_fields = ['name', 'tab__display_name']
    inlines = [ShopProductInline]


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'is_active', 'created_at']
    list_filter = ['is_active', 'category__tab', 'category']
    search_fields = ['name', 'category__name']
