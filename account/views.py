from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from account.models import CustomUser, Address
from account.serializers import CustomuserRegisterSerializer, CustomuserLoginSerializer

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
    


    

