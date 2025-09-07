from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, DetallePedidoViewSet, CompraViewSet, DetalleCompraViewSet, PedidoRecepcionViewSet

# Crear un router y registrar las vistas
router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'compras', CompraViewSet)
router.register(r'detalles-compra', DetalleCompraViewSet)
router.register(r'pedidos-recepcion', PedidoRecepcionViewSet, basename='pedidos-recepcion')

urlpatterns = [
    path('', include(router.urls)),
]