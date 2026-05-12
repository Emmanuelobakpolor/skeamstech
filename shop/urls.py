from django.urls import path
from .views import (
    ShopTabsListView,
    ShopCategoryListView,
    ShopProductListView,
    ShopSearchView,
)

urlpatterns = [
    path('tabs/', ShopTabsListView.as_view()),
    path('categories/', ShopCategoryListView.as_view()),
    path('products/', ShopProductListView.as_view()),
    path('search/', ShopSearchView.as_view()),
]
