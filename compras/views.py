# views.py
from rest_framework import viewsets
from .serializers import PedidoSerializer, DetallePedidoSerializer, CompraSerializer, DetalleCompraSerializer
from .models import Pedido, DetallePedido, Compra, DetalleCompra
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import permissions
from core.views import AuditableModelViewSet


class PedidoViewSet(PaginacionYAllDataMixin, AuditableModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class DetallePedidoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompraViewSet(PaginacionYAllDataMixin, AuditableModelViewSet):
    queryset = Compra.objects.all() 
    serializer_class = CompraSerializer
    permission_classes = [permissions.IsAuthenticated]


class DetalleCompraViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [permissions.IsAuthenticated]


