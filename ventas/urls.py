from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VentaView, DetalleVentaView, FacturaVentaView, ClienteView

# Crear un router y registrar las vistas
router = DefaultRouter()
router.register(r'clientes', ClienteView)
router.register(r'ventas', VentaView)
router.register(r'detalles-venta', DetalleVentaView)
router.register(r'facturas-venta', FacturaVentaView)

urlpatterns = [
    path("", include(router.urls)),  # Incluir las URLs del router
]
