from django.urls import path
from account.views import RegisterUserAPIView, LoginUserAPIView, LogoutUserAPIView, RequestOTPAPIView,VerifyOTPAPIView


urlspatterns = [
    path('auth/register/', RegisterUserAPIView.as_view()),
    path('auth/login/', LoginUserAPIView.as_view()),
    path('auth/logout/', LogoutUserAPIView.as_view()),
    path('auth/otp/', RequestOTPAPIView.as_view()),
    path('auth/confirm_otp/', VerifyOTPAPIView.as_view()),
]