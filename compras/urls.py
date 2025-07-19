from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, DetallePedidoViewSet, RecepcionPedidoViewSet, DetalleRecepcionViewSet, CompraViewSet

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'detalles-pedido', DetallePedidoViewSet)
router.register(r'recepciones', RecepcionPedidoViewSet)
router.register(r'detalles-recepcion', DetalleRecepcionViewSet)
router.register(r'compras', CompraViewSet)

urlpatterns = [
    path('', include(router.urls)),
]