from rest_framework import serializers
from shop.models import Product, ProductImage, Category, Store, StoreItem


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


class StoreSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'seller']


class StoreItemSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    store_id = serializers.PrimaryKeyRelatedField(
        queryset=Store.objects.all(), source='store', write_only=True
    )
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    class Meta:
        model = StoreItem
        fields = [
            'id', 'store', 'product', 'store_id', 'product_id', 'price', 
            'discount_price', 'stock', 'is_active', 'created_at', 'updated_at'
        ]
