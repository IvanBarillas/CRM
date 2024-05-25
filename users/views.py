# users/views.py
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils.timezone import make_aware, now
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .serializers import UserSerializer, UserCreateSerializer, RequestAccessSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import uuid
import logging



logger = logging.getLogger(__name__)



class UserRegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny] 

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
    
class RequestAccessTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestAccessSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user, created = CustomUser.objects.get_or_create(email=email, user_type='final')
            if created:
                user.first_name = "User"
                user.last_name = "Final"
                user.save()

            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # Enviar correo con el token
            send_mail(
                'Tu enlace de acceso',
                f'Por favor haz clic en el siguiente enlace para acceder a tu cuenta:\n\n'
                f'{settings.SITE_URL}/api/users/access/{token}/',  # Asegúrate de que esta URL sea correcta
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({'detail': 'Correo enviado con el enlace de acceso'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AccessTokenLoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token, *args, **kwargs):
        try:
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            jti = validated_token.get('jti')

            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                logger.warning("El token ya ha sido utilizado o incluido en la lista negra")
                return redirect('admin:login')

            user = jwt_auth.get_user(validated_token)
            login(request, user)
            logger.info(f"Usuario {user.email} autenticado exitosamente")

            expires_at = make_aware(datetime.fromtimestamp(validated_token['exp']))
            outstanding_token, created = OutstandingToken.objects.get_or_create(
                jti=jti,
                defaults={'token': validated_token, 'expires_at': expires_at, 'user': user}
            )

            if created:
                BlacklistedToken.objects.create(token=outstanding_token)
                logger.info("Token invalidado exitosamente y añadido a la lista negra con información del usuario.")
            else:
                logger.warning("El token ya está en la lista de OutstandingTokens")

            return redirect('home')  # Redirigir a la página de inicio tras un login exitoso
        except InvalidToken as e:
            logger.error(f"Error de validación de token: {e}")
            return redirect('admin:login')  # Redirigir a la página de login del admin en caso de token inválido o expirado
        except Exception as e:
            logger.error(f"Error desconocido: {str(e)}")
            return redirect('admin:login')  # Redirigir a la página de login del admin en caso de error desconocido