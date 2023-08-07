from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Brand, Category, Product
from .serializers import BrandSerializer, CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ViewSet):
    """
    Viewset for viewing all categories
    """

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=CategorySerializer, responses=CategorySerializer)
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=CategorySerializer, responses=CategorySerializer)
    def retrieve(self, request, pk):
        try:
            retrieved_category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(retrieved_category)
        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """
    Viewset for viewing all brands
    """

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=BrandSerializer, responses=BrandSerializer)
    def create(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=BrandSerializer, responses=BrandSerializer)
    def retrieve(self, request, pk):
        try:
            retrieved_brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BrandSerializer(retrieved_brand)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """
    Viewset for viewing all products
    """

    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def create(self, request, *args, **kwargs):
        new_data = request.data
        brand_name = new_data["brand"]["names"]
        category_name = new_data["category"]["names"]

        newbrand, _ = Brand.objects.get_or_create(names=brand_name)
        newcategory, _ = Category.objects.get_or_create(names=category_name)

        product_data = {
            "names": new_data["names"],
            "description": new_data["description"],
            "is_digital": new_data["is_digital"],
            "brand": newbrand,
            "category": newcategory,
        }
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # retrieve each product separately
    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def retrieve(self, request, pk):
        try:
            retrieved_product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ProductSerializer(retrieved_product)
        return Response(serializer.data)
