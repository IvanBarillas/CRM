from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import HomePageView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/', HomePageView.as_view(), name='home'),  
]


#Cargar las archivos medias
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)