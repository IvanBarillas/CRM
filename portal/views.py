# portal/views.py
from datetime import datetime
from django.shortcuts import redirect
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from users.models import EndUser, ManagerUser, CustomUser, Profile
from .serializers import RequestAccessSerializer
from .tasks import send_access_enduser_email, send_admin_login_email
import logging

logger = logging.getLogger(__name__)

class RequestAccessTokenAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RequestAccessSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Verificar si el email existe en ManagerUser o es un superusuario
            if ManagerUser.objects.filter(email=email).exists() or CustomUser.objects.filter(email=email, is_superuser=True).exists():
                send_admin_login_email.delay(email)
                return Response({'detail': 'Los administradores deben ingresar por el panel de administración'}, status=status.HTTP_403_FORBIDDEN)
            
            user, created = EndUser.objects.get_or_create(email=email)
            if created:
                user.first_name = "User"
                user.last_name = "Final"
                user.save()

            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            # Enviar correo con el token de forma asíncrona
            send_access_enduser_email.delay(email, token)

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

            # Asegúrate de que el perfil existe
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)

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
