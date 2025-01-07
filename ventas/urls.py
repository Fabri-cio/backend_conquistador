from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VentaViewSet, DetalleVentaViewSet

# Crear un router y registrar las vistas
router = DefaultRouter()
router.register(r'ventas', VentaViewSet)
router.register(r'detalles-venta', DetalleVentaViewSet)

urlpatterns = [
    path("", include(router.urls)),  # Incluir las URLs del router
]
