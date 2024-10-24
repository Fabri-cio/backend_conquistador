from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import UsuarioView

router = routers.DefaultRouter()

router.register(r'usuarios', UsuarioView)  # Rutas para usuarios

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include_docs_urls(title="Usuarios API"))
]
