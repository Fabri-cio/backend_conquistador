# views.py
from rest_framework import viewsets
from .serializers import PedidoSerializer, DetallePedidoSerializer, CompraSerializer, DetalleCompraSerializer
from .models import Pedido, DetallePedido, Compra, DetalleCompra
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import permissions


class PedidoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class DetallePedidoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompraViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Compra.objects.all() 
    serializer_class = CompraSerializer
    permission_classes = [permissions.IsAuthenticated]


class DetalleCompraViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    permission_classes = [permissions.IsAuthenticated]


