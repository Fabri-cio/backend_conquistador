import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import inventarios.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_crud_api.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP normal
    "websocket": AuthMiddlewareStack(
        URLRouter(
            inventarios.routing.websocket_urlpatterns
        )
    ),
})
