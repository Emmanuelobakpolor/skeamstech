from django.db.models import Q, Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import status
from .models import ShopTab, ShopCategory, ShopProduct
from .serializers import (
    ShopTabSerializer,
    ShopCategorySerializer,
    ShopProductSerializer,
    AdminShopTabSerializer,
    AdminShopCategorySerializer,
    AdminShopProductSerializer,
)


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


# ============================================================================
# ADMIN VIEWS (CRUD endpoints)
# ============================================================================


class AdminShopTabListCreateView(APIView):
    """Admin: GET all tabs (including inactive) + POST to create new tab"""
    permission_classes = [AllowAny]

    def get(self, request):
        tabs = ShopTab.objects.all().order_by('order', 'name')
        serializer = AdminShopTabSerializer(tabs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminShopTabSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminShopTabDetailView(APIView):
    """Admin: GET/PUT/PATCH/DELETE single tab"""
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return ShopTab.objects.get(pk=pk)
        except ShopTab.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminShopTabSerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminShopTabSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminShopTabSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminShopCategoryListCreateView(APIView):
    """Admin: GET categories (supports ?tab=<id> filter) + POST to create"""
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = ShopCategory.objects.all()
        tab_id = request.query_params.get('tab')
        if tab_id:
            queryset = queryset.filter(tab_id=tab_id)
        queryset = queryset.order_by('tab', 'name')
        serializer = AdminShopCategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminShopCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminShopCategoryDetailView(APIView):
    """Admin: GET/PUT/PATCH/DELETE single category"""
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return ShopCategory.objects.get(pk=pk)
        except ShopCategory.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminShopCategorySerializer(obj)
        return Response(serializer.data)

    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminShopCategorySerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminShopCategorySerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminShopProductListCreateView(APIView):
    """Admin: GET products (supports ?category=<id> filter) + POST to create with image"""
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        queryset = ShopProduct.objects.all().select_related('category')
        category_id = request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        queryset = queryset.order_by('category', 'name')
        serializer = AdminShopProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminShopProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminShopProductDetailView(APIView):
    """Admin: GET/PATCH/DELETE single product"""
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self, pk):
        try:
            return ShopProduct.objects.get(pk=pk)
        except ShopProduct.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminShopProductSerializer(obj, context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AdminShopProductSerializer(
            obj,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response(status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
