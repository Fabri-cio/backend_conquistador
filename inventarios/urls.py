from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlmacenViewSet, TipoMovimientoViewSet, InventarioViewSet, MovimientoViewSet, InventarioVentasViewSet, InventarioABCViewSet

router = DefaultRouter()
router.register(r'almacenes', AlmacenViewSet)
router.register(r'tipos-movimiento', TipoMovimientoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'inventarios-ventas', InventarioVentasViewSet, basename='inventarios-ventas')
router.register(r'inventarios-abc', InventarioABCViewSet, basename='inventarios-abc')

urlpatterns = [
    path('', include(router.urls)),
]