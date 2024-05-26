# portal/urls.py
from django.urls import path
from .views import AccessTokenLoginView, RequestAccessTokenAPIView

urlpatterns = [
    path('request-access/', RequestAccessTokenAPIView.as_view(), name='request_access_token'),
    path('access/<str:token>/', AccessTokenLoginView.as_view(), name='access_token_login'),

    #Url de renderizados de templates.
    
]
