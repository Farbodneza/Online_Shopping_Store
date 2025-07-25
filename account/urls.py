from django.urls import path, include
from account.views import RegisterUserAPIView, LoginUserAPIView, LogoutUserAPIView, RequestOTPAPIView,VerifyOTPAPIView, ProfileManagmentAPIView, AddressManagerAPIViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'profiles', ProfileManagmentAPIView, basename='profile')
router.register(r'addresses', AddressManagerAPIViewSet, basename='address')


urlspatterns = [
    path('auth/register/', RegisterUserAPIView.as_view()),
    path('auth/login/', LoginUserAPIView.as_view()),
    path('auth/logout/', LogoutUserAPIView.as_view()),
    path('auth/otp/', RequestOTPAPIView.as_view()),
    path('auth/confirm_otp/', VerifyOTPAPIView.as_view()),
    path('', include(router.urls)),
]