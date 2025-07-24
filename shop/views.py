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
from rest_framework.permissions import IsAuthenticated , AllowAny, IsAdminUser
from shop.permissions import IsSeller, IsShopOwner
from shop.serializers import (ProductSerializer, 
                              CategorySerializer
                            )


class CategoryAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        category_data = self.get_serializer(instance).data
        products = instance.products.all() 
        product_data = ProductSerializer(products, many=True, context={'request': request}).data

        return Response({
            "category": category_data,
            "products": product_data
        })


class ManageCategoryAPIViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.action == 'List':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsSeller]
        return [permission() for permission in permission_classes]


class ManageProductAPIViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSeller]


class ManageStoreAPIViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsSeller, IsShopOwner]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsSeller]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]



