from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VentaView, DetalleVentaView

# Crear un router y registrar las vistas
router = DefaultRouter()
router.register(r'ventas', VentaView)
router.register(r'detalles-venta', DetalleVentaView)

urlpatterns = [
    path("", include(router.urls)),  # Incluir las URLs del router
]
