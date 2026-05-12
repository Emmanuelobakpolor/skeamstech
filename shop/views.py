from django.db.models import Q, Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import ShopTab, ShopCategory, ShopProduct
from .serializers import ShopTabSerializer, ShopCategorySerializer, ShopProductSerializer


class ShopTabsListView(APIView):
    """Returns all tabs with their nested categories and products"""
    permission_classes = [AllowAny]

    def get(self, request):
        tabs = ShopTab.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                'categories',
                queryset=ShopCategory.objects.filter(is_active=True).prefetch_related(
                    Prefetch(
                        'products',
                        queryset=ShopProduct.objects.filter(is_active=True)
                    )
                )
            )
        )
        serializer = ShopTabSerializer(tabs, many=True, context={'request': request})
        return Response(serializer.data)


class ShopCategoryListView(APIView):
    """Legacy endpoint - returns all categories (deprecated, use /tabs/ instead)"""
    permission_classes = [AllowAny]

    def get(self, request):
        categories = ShopCategory.objects.filter(is_active=True).prefetch_related(
            Prefetch(
                'products',
                queryset=ShopProduct.objects.filter(is_active=True)
            )
        )
        serializer = ShopCategorySerializer(
            categories,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class ShopProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        category_id = request.query_params.get('category')
        queryset = ShopProduct.objects.filter(
            is_active=True,
            category__is_active=True
        ).select_related('category')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        serializer = ShopProductSerializer(
            queryset,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


class ShopSearchView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response([])

        products = ShopProduct.objects.filter(
            is_active=True,
            category__is_active=True
        ).filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(application__icontains=query)
            | Q(category__name__icontains=query)
        ).select_related('category')

        serializer = ShopProductSerializer(
            products,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
