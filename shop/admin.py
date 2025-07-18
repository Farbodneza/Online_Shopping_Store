from django.contrib import admin
from shop.models import (
    Category, Product, ProductImage, Store, StoreItem, 
    Order, OrderItem, Cart, CartItem, Review
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'best_price', 'stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'categories')
    search_fields = ('name',)
    # filter_horizontal = ('categories',)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller')
    search_fields = ('name', 'seller__username')

@admin.register(StoreItem)
class StoreItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'store', 'price', 'stock', 'is_active')
    list_filter = ('is_active', 'store')
    search_fields = ('product__name', 'store__name')
    autocomplete_fields = ['product', 'store']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'customer__username')
    readonly_fields = ('created_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_active')
    search_fields = ('user__username',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('product__name', 'user__username')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'store_item', 'quantity', 'price')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'store_item', 'quantity')

