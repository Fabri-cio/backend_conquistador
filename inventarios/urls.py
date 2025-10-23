from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlmacenViewSet, TipoMovimientoViewSet, InventarioViewSet, MovimientoViewSet, InventarioVentasViewSet, InventarioABCViewSet, InventarioCarritoViewSet, NotificacionViewSet, InventarioListViewSet, AlmacenListViewSet, MovimientoListViewSet, AlmacenSelectViewSet, InventarioSelectViewSet, TiposMovimientoSelectViewSet, InventarioPedidosViewSet

router = DefaultRouter()
router.register(r'almacenes', AlmacenViewSet)
router.register(r'tipos-movimiento', TipoMovimientoViewSet)
router.register(r'inventarios', InventarioViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'inventarios-ventas', InventarioVentasViewSet, basename='inventarios-ventas')
router.register(r'inventarios-abc', InventarioABCViewSet, basename='inventarios-abc')
router.register(r'inventarios-carrito', InventarioCarritoViewSet, basename='inventarios-carrito')
router.register(r'notificaciones', NotificacionViewSet, basename='notificaciones')
router.register(r'inventarios-list', InventarioListViewSet, basename='inventarios-list')
router.register(r'almacenes-list', AlmacenListViewSet, basename='almacenes-list')
router.register(r'movimientos-list', MovimientoListViewSet, basename='movimientos-list')
router.register(r'inventarios-pedidos', InventarioPedidosViewSet, basename='inventarios-pedidos')

urlpatterns = [
    path('', include(router.urls)),

    path('inventarios-select/', InventarioSelectViewSet.as_view(), name='inventarios-select'),
    path('tipos-movimiento-select/', TiposMovimientoSelectViewSet.as_view(), name='tipos-movimiento-select'),
    path('almacenes-select/', AlmacenSelectViewSet.as_view(), name='almacenes-select'),
]