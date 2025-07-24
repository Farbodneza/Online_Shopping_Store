from rest_framework import serializers
from shop.models import Product, shop, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields= "__all__"


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    class Meta:
        model = Category
        fields= ['name', 'parent', 'description', 'image', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(source='productimage_set', many=True)
    class Meta:
        model = Product
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = shop 
        fields= "__all__"






