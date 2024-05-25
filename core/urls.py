from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import HomePageView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import AccessTokenLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/', HomePageView.as_view(), name='home'),

    #Url de API users
    path('api/users/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('access/<str:token>/', AccessTokenLoginView.as_view(), name='access_token_login'),
]


#Cargar las archivos medias
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    