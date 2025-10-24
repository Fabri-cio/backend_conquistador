from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, DetallePedidoViewSet, CompraViewSet, DetalleCompraViewSet, PedidoRecepcionViewSet, DetallesCompraPedidoViewSet, PedidoListViewSet, CompraListViewSet

# Crear un router y registrar las vistas
router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'detalles-compra', DetalleCompraViewSet)
router.register(r'pedidos-recepcion', PedidoRecepcionViewSet, basename='pedidos-recepcion')
router.register(r'detalles-compra-pedido', DetallesCompraPedidoViewSet, basename='detalles-compra-pedido')
router.register(r'pedidos-list', PedidoListViewSet, basename='pedidos-list')
router.register(r'compras-list', CompraListViewSet, basename='compras-list')

urlpatterns = [
    path('', include(router.urls)),
]