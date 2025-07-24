from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from shop.models import Product, Store, StoreItem, ProductImage, Category
from django.core.cache import cache
from rest_framework.decorators import action
from django.http import HttpResponse
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated , AllowAny, IsAdminUser, PermissionDenied
from shop.permissions import IsSeller, IsShopOwner, CanAddShopItem
from shop.serializers import (ProductSerializer, 
                              CategorySerializer,
                              StoreItemSerializer,
                                StoreSerializer,
                            )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated, IsSeller]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        category_data = self.get_serializer(instance).data
        products = instance.products.filter(is_active=True)
        product_data = ProductSerializer(products, many=True, context={'request': request}).data
        
        return Response({
            "category": category_data,
            "products": product_data
        })


class ManageProductAPIViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]


class ManageStoreAPIViewSet(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    

    def get_queryset(self):
        if self.request.user.is_authenticated and hasattr(self.request.user, 'store'):
            return Store.objects.filter(seller=self.request.user)
        return Store.objects.all()


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSeller, IsShopOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    

    def perform_create(self, serializer):
        user= self.request.user
        if hasattr(user, 'store'):
            raise PermissionDenied("You already own a store.")
        serializer.save(seller=user)
        user.objects.update(is_seller = True)
        

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        store_data = self.get_serializer(instance).data
        
        store_items = instance.items.filter(is_active=True)
        item_data = StoreItemSerializer(store_items, many=True, context={'request': request}).data

        return Response({
            "store": store_data,
            "items": item_data
        })

    
class ManageStoreItemsAPIViewSet(viewsets.ModelViewSet):
    queryset = StoreItem.objects.filter(is_active=True)
    serializer_class = StoreItemSerializer
    permission_classes = [IsAuthenticated, CanAddShopItem]
    def perform_create(self, serializer):
        serializer.save(store=self.request.user.store)
        return super().perform_create(serializer)


