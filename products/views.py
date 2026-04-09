from rest_framework import viewsets, filters
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView

from .models import Category, SubCategory, Product
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ProductSerializer,
    ProductCreateUpdateSerializer
)
from core.response import success_response, error_response

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        return [AllowAny()] if self.action in ['list', 'retrieve'] else [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        return success_response("Categories fetched successfully",
                                self.get_serializer(self.get_queryset(), many=True).data)

    def retrieve(self, request, *args, **kwargs):
        return success_response("Category fetched successfully",
                                [self.get_serializer(self.get_object()).data])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Category created", [serializer.data], 201)
        return error_response("Category creation failed", serializer.errors)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Category updated", [serializer.data])
        return error_response("Update failed", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return success_response("Category deleted", [], 204)
    

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.select_related('category')
    serializer_class = SubCategorySerializer

    def get_permissions(self):
        return [AllowAny()] if self.action in ['list', 'retrieve'] else [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        category_id = request.query_params.get('category_id')

        if category_id:
            qs = qs.filter(category_id=category_id)

        return success_response("Subcategories fetched",
                                self.get_serializer(qs, many=True).data)
    


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'subcategory')
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        return [AllowAny()] if self.action in ['list', 'retrieve'] else [IsAdminUser()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        category_id = self.request.query_params.get('category_id')
        subcategory_id = self.request.query_params.get('subcategory_id')

        if category_id:
            qs = qs.filter(category_id=category_id)
        if subcategory_id:
            qs = qs.filter(subcategory_id=subcategory_id)

        return qs

    def list(self, request, *args, **kwargs):
        return success_response("Products fetched",
                                self.get_serializer(self.get_queryset(), many=True).data)

    def retrieve(self, request, *args, **kwargs):
        return success_response("Product fetched",
                                [self.get_serializer(self.get_object()).data])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Product created", [serializer.data], 201)
        return error_response("Creation failed", serializer.errors)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response("Product updated", [serializer.data])
        return error_response("Update failed", serializer.errors)

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return success_response("Product deleted", [], 204)
    



class FeaturedProductView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_featured=True)
        serializer = ProductSerializer(products, many=True)

        return success_response("Featured products fetched", serializer.data)
    

