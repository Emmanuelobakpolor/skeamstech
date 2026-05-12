from django.urls import path
from .views import (
    ShopTabsListView,
    ShopCategoryListView,
    ShopProductListView,
    ShopSearchView,
    AdminShopTabListCreateView,
    AdminShopTabDetailView,
    AdminShopCategoryListCreateView,
    AdminShopCategoryDetailView,
    AdminShopProductListCreateView,
    AdminShopProductDetailView,
    AdminProductImageListCreateView,
    AdminProductImageDetailView,
    AdminProductModelListCreateView,
    AdminProductModelDetailView,
    AdminProductModelImageListCreateView,
    AdminProductModelImageDetailView,
)

urlpatterns = [
    # Read-only public endpoints
    path('tabs/', ShopTabsListView.as_view()),
    path('categories/', ShopCategoryListView.as_view()),
    path('products/', ShopProductListView.as_view()),
    path('search/', ShopSearchView.as_view()),
    # Admin CRUD endpoints
    path('admin/tabs/', AdminShopTabListCreateView.as_view()),
    path('admin/tabs/<int:pk>/', AdminShopTabDetailView.as_view()),
    path('admin/categories/', AdminShopCategoryListCreateView.as_view()),
    path('admin/categories/<int:pk>/', AdminShopCategoryDetailView.as_view()),
    path('admin/products/', AdminShopProductListCreateView.as_view()),
    path('admin/products/<int:pk>/', AdminShopProductDetailView.as_view()),
    # Product image sub-resources
    path('admin/products/<int:product_pk>/images/', AdminProductImageListCreateView.as_view()),
    path('admin/products/<int:product_pk>/images/<int:image_pk>/', AdminProductImageDetailView.as_view()),
    # Product model sub-resources
    path('admin/products/<int:product_pk>/models/', AdminProductModelListCreateView.as_view()),
    path('admin/products/<int:product_pk>/models/<int:model_pk>/', AdminProductModelDetailView.as_view()),
    # Product model image sub-resources
    path('admin/products/<int:product_pk>/models/<int:model_pk>/images/', AdminProductModelImageListCreateView.as_view()),
    path('admin/products/<int:product_pk>/models/<int:model_pk>/images/<int:image_pk>/', AdminProductModelImageDetailView.as_view()),
]
