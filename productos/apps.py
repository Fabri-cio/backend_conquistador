from django.apps import AppConfig
from django.conf import settings
import os

class ProductosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'productos'

    def ready(self):
        media_subdirs = ['proveedores', 'categorias', 'productos']
        for subdir in media_subdirs:
            path = os.path.join(settings.MEDIA_ROOT, subdir)
            os.makedirs(path, exist_ok=True)
                
