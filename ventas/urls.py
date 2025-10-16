from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VentaView, DetalleVentaView, ComprobanteVentaView, ClienteView, VentaReporteView, VentasPorInventarioViewSet

# Crear un router y registrar las vistas
router = DefaultRouter()
router.register(r'clientes', ClienteView)
router.register(r'ventas', VentaView)
router.register(r'detalles-venta', DetalleVentaView)
router.register(r'comprobantes-venta', ComprobanteVentaView)
router.register(r'ventas-reporte', VentaReporteView, basename='ventas-reporte')
router.register(r'ventas-por-inventario', VentasPorInventarioViewSet, basename='ventas-por-inventario')

urlpatterns = [
    path("", include(router.urls)),  # Incluir las URLs del router
]
