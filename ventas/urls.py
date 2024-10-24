from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import ClienteView, VentaView, DetalleVentaView

router = routers.DefaultRouter()

router.register(r'clientes', ClienteView)  # Rutas para categorías
router.register(r'ventas', VentaView)  # Rutas para productos
router.register(r'detalles-ventas', DetalleVentaView)  # Rutas para productos

urlpatterns = [
    path("", include(router.urls)),
    path("docs/", include_docs_urls(title="Ventas API"))
]
