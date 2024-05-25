# users/urls.py
from django.urls import path
from .views import UserRegisterAPIView, UserProfileAPIView, UserTypeRedirectAPIView, AccessTokenLoginView, RequestAccessTokenAPIView

urlpatterns = [
    path('register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('profile/', UserProfileAPIView.as_view(), name='user_profile'),
    path('redirect/', UserTypeRedirectAPIView.as_view(), name='user_redirect'),
    path('access/<str:token>/', AccessTokenLoginView.as_view(), name='access_token_login'),
    path('request-access/', RequestAccessTokenAPIView.as_view(), name='request_access_token'),
]