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
    def retrieve(self, request, pk=None):
        try:
            retrieved_category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(retrieved_category)
        return Response(serializer.data)

    @extend_schema(request=CategorySerializer, responses=CategorySerializer)
    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=CategorySerializer, responses=CategorySerializer)
    def partial_update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    def retrieve(self, request, pk=None):
        try:
            retrieved_brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BrandSerializer(retrieved_brand)
        return Response(serializer.data)

    @extend_schema(request=BrandSerializer, responses=BrandSerializer)
    def update(self, request, pk):
        try:
            requested_data = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "The Brand you requested can not be found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BrandSerializer(requested_data, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=BrandSerializer, responses=BrandSerializer)
    def partial_update(self, request, pk):
        try:
            requested_data = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"error": "The Brand you requested can not be found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BrandSerializer(requested_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        try:
            data_to_destroy = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found"}, status=status.HTTP_400_BAD_REQUEST)

        data_to_destroy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
        brand_name = new_data["brand"]
        category_name = new_data["category"]

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

    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def update(self, request, pk):
        try:
            requested_data = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product does not exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        updated_data = request.data
        brand_name = updated_data["brand"]
        updated_brand, _ = Brand.objects.get_or_create(names=brand_name)
        category_name = updated_data["category"]
        updated_category, _ = Category.objects.get_or_create(names=category_name)

        product_data = {
            "names": updated_data["names"],
            "description": updated_data["description"],
            "is_digital": updated_data["is_digital"],
            "brand": updated_brand,
            "category": updated_category,
        }
        serializer = ProductSerializer(requested_data, product_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(request=ProductSerializer, responses=ProductSerializer)
    def partial_update(self, request, pk):
        try:
            requested_data = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product does not exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        updated_data = request.data
        brand_name = updated_data["brand"]
        updated_brand, _ = Brand.objects.get_or_create(names=brand_name)
        category_name = updated_data["category"]
        updated_category, _ = Category.objects.get_or_create(names=category_name)

        product_data = {
            "names": updated_data["names"],
            "description": updated_data["description"],
            "is_digital": updated_data["is_digital"],
            "brand": updated_brand,
            "category": updated_category,
        }
        serializer = ProductSerializer(requested_data, product_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses=ProductSerializer)
    def destroy(self, request, pk=None):
        try:
            data_to_destroy = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        data_to_destroy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
