# inventarios/routing.py
from django.urls import re_path
from .consumers import NotificacionConsumer

websocket_urlpatterns = [
    re_path(r'ws/notificaciones/$', NotificacionConsumer.as_asgi()),
]
