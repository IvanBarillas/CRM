#users/views.py
from django.views.generic.base import TemplateView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EndUser, ManagerUser
from .serializers import EndUserSerializer

class UserRegisterAPIView(generics.CreateAPIView):
    queryset = EndUser.objects.all()
    serializer_class = EndUserSerializer
    permission_classes = [AllowAny]

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = EndUser.objects.all()
    serializer_class = EndUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserTypeRedirectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        if isinstance(user, ManagerUser):
            return Response({'detail': 'Redirect to internal dashboard'}, status=status.HTTP_200_OK)
        elif isinstance(user, EndUser):
            return Response({'detail': 'Redirect to final user dashboard'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)


# vistas de Renderizado de Templates

class AccountSettingsAccountView(TemplateView):
    template_name = 'users/account_settings_account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Configuracón de la Cuenta'        
        return context
    