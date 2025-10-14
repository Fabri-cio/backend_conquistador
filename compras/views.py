# views.py
from rest_framework import viewsets
from .serializers import PedidoSerializer, DetallePedidoSerializer, CompraSerializer, DetalleCompraSerializer, PedidoRecepcionSerializer, DetallesCompraPedidoSerializer
from .models import Pedido, DetallePedido, Compra, DetalleCompra
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import permissions
from core.views import AuditableModelViewSet
from core.mixins import FiltradoPorUsuarioInteligenteMixin

class PedidoRecepcionViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('id')
    serializer_class = PedidoRecepcionSerializer
    # permission_classes = [permissions.IsAuthenticated]

class PedidoViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
    queryset = Pedido.objects.all().order_by('id')
    serializer_class = PedidoSerializer
    # permission_classes = [permissions.IsAuthenticated]


class DetallePedidoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all().order_by('id')
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompraViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
    queryset = Compra.objects.all().order_by('id')
    serializer_class = CompraSerializer
    # permission_classes = [permissions.IsAuthenticated]


class DetalleCompraViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.all().order_by('id')
    serializer_class = DetalleCompraSerializer
    permission_classes = [permissions.IsAuthenticated]

class DetallesCompraPedidoViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all().order_by('id')
    serializer_class = DetallesCompraPedidoSerializer
    # permission_classes = [permissions.IsAuthenticated]


