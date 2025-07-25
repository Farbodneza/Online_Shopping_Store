from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from shop.models import Product, Store, StoreItem, ProductImage, Category
from django.core.cache import cache
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated , AllowAny, IsAdminUser
from shop.permissions import IsSeller, IsShopOwner, CanAddShopItem
from shop.serializers import (ProductSerializer, 
                              CategorySerializer,
                              StoreItemSerializer,
                                StoreSerializer,
                            )


class CategoryAPIViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated, IsSeller]
        return super().get_permissions()

    def _get_all_descendants(self, category):
        descendants = list(category.children.filter(is_active=True))
        for child in descendants:
            descendants.extend(self._get_all_descendants(child))
        return descendants
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        category_path = []
        current_category = instance
        while current_category is not None:
            category_path.append(current_category)
            current_category = current_category.parent
        
        path_for_display = list(reversed(category_path))
        path_serializer = self.get_serializer(path_for_display, many=True)
        
        direct_subcategories = instance.children.filter(is_active=True)
        subcategories_serializer = self.get_serializer(direct_subcategories, many=True)

        categories_to_filter = [instance] + self._get_all_descendants(instance)
        
        products = Product.objects.filter(categories__in=categories_to_filter, is_active=True).distinct()
        product_data = ProductSerializer(products, many=True, context={'request': request}).data
        
        return Response({
            "category_path": path_serializer.data,
            "sub_categories": subcategories_serializer.data,
            "products": product_data
        })

class ProductAPIViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]


class StoreAPIViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer

    def get_queryset(self):
        return Store.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSeller, IsShopOwner]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        user= self.request.user
        serializer.save(seller=user)
        if not user.is_seller:
            user.is_seller = True
            user.save()
        
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        store_data = self.get_serializer(instance).data
        
        store_items = instance.items.filter(is_active=True)
        item_data = StoreItemSerializer(store_items, many=True, context={'request': request}).data

        return Response({
            "store": store_data,
            "items": item_data
        })

    
class StoreItemsAPIViewSet(viewsets.ModelViewSet):
    serializer_class = StoreItemSerializer
    permission_classes = [IsAuthenticated, CanAddShopItem]

    def get_queryset(self):
        return StoreItem.objects.all()

# {
# "name":"feri",
# "description":"farbod's shop"
# }