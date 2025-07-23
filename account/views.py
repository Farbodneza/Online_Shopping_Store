from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from account.models import CustomUser, Address
from django.core.cache import cache
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated , AllowAny, IsAdminUser
from account.permissions import IsProfileOwnerOrAdmin
from account.utils import send_custom_email
from account.serializers import (CustomuserRegisterSerializer, 
                                CustomuserLoginSerializer, 
                                OTPRequestSerializer,
                                OTPVerifySerializer,
                                CustomUserEditProfile
                            )
import random

class RegisterUserAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomuserRegisterSerializer


class LoginUserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomuserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            user_serializer = CustomuserRegisterSerializer(user)
            login(request, user)  
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
    

class LogoutUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        print(request.user)
        logout(request)
        print(request.user)
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)
    

class RequestOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):   
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = CustomUser.objects.get(email=email)
        except:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        otp_code = str(random.randint(100000, 999999))
        cache.set(f'otp_{email}', otp_code, timeout=120)

        subject = 'Hello from Farbod Shop'
        message = f'This is your OTP : {otp_code}'
        recipient_list = [email] 

        send_custom_email(subject, message, recipient_list)

        print(f"OTP for {email}: {otp_code}")

        return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        otp_from_user = serializer.validated_data['otp']

        stored_otp = cache.get(f'otp_{email}')

        if not stored_otp:
            return Response({'error': 'OTP has expired or is invalid.'}, status=status.HTTP_400_BAD_REQUEST)

        if stored_otp != otp_from_user:
            return Response({'error': 'Invalid OTP code.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        refresh = RefreshToken.for_user(user)

        login(request, user)
        
        cache.delete(f'otp_{email}')

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)


class ProfileManagmentAPIView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CustomUserEditProfile
        return CustomuserRegisterSerializer
    def get_permissions(self):
        if self.action == 'list':
            permision_classes = [IsAdminUser]
        elif self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            permission_classes = [IsAuthenticated, IsProfileOwnerOrAdmin] 
        else:
            permission_classes = [IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]