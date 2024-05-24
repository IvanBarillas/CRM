# core/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# establecer la variable de entorno predeterminada para la configuración de celery para 'settings.py'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Usar el namespace 'CELERY' para que todas las configuraciones de Celery tengan el prefijo 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Cargar módulos de tareas de todas las aplicaciones registradas
app.autodiscover_tasks()