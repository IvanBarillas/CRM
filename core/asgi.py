# core/asgi.py

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Importar get_asgi_application() después de configurar la variable de entorno
django_asgi_app = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
#import activity.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,    
})
