# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer, UserCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserTypeRedirectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == 'internal':
            return Response({'detail': 'Redirect to internal dashboard'}, status=status.HTTP_200_OK)
        elif user.user_type == 'final':
            return Response({'detail': 'Redirect to final user dashboard'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)
    
class AccessTokenLoginView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            user = jwt_auth.get_user(validated_token)
            login(request, user)
            return redirect('user_tickets')
        except InvalidToken:
            return Response({'detail': 'Token inválido o expirado'}, status=status.HTTP_400_BAD_REQUEST)
