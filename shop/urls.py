from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryAPIViewSet,
    ProductAPIViewSet,
    StoreAPIViewSet,
    StoreItemsAPIViewSet
)


router = DefaultRouter()

router.register(r'categories', CategoryAPIViewSet, basename='category')
router.register(r'products', ProductAPIViewSet, basename='product')
router.register(r'stores', StoreAPIViewSet, basename='store')
router.register(r'store-items', StoreItemsAPIViewSet, basename='storeitem')


urlpatterns = [
    path('', include(router.urls)),
]
