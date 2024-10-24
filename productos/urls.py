from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import ProductoView, CategoriaView

router = routers.DefaultRouter()

router.register(r'categorias', CategoriaView)  # Rutas para manejar categorías
router.register(r'productos', ProductoView)  # Rutas para manejar productos

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include_docs_urls(title="Productos API"))
]
