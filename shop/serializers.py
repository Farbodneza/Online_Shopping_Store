from rest_framework import serializers
from shop.models import Product, shop, ProductImage, Category, Store


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields= ['id', 'image']


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='parent', write_only=True, required=False, allow_null=True
    )
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'parent_id', 'description', 'image', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'best_price', 'stock', 'rating', 
            'categories', 'images', 'is_active', 'created_at', 'updated_at'
        ]


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = shop 
        fields= "__all__"


class StoreItemSerializer(serializers.ModelSerializer):
    store = ShopSerializer()
    product = ProductSerializer()
    class Meta:
        model = Store
        fileds = ['store', 'product', 'price', 'discount_price', 'stock', 'is_active', 'created_at', 'updated_at']




