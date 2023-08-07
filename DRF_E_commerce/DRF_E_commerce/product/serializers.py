from rest_framework import serializers

from .models import Brand, Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["names"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    # Instead of using BrandSerializer and CategorySerializer here,
    # you should specify the respective field names as 'slug' or 'id'
    brand = serializers.SlugRelatedField(slug_field="names", queryset=Brand.objects.all())
    category = serializers.SlugRelatedField(slug_field="names", queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = "__all__"
