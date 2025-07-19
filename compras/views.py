from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Pedido, DetallePedido, RecepcionPedido, DetalleRecepcion, Compra
from .serializers import PedidoSerializer, DetallePedidoSerializer, RecepcionPedidoSerializer, DetalleRecepcionSerializer, CompraSerializer


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer


class DetallePedidoViewSet(viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all()
    serializer_class = DetallePedidoSerializer


class RecepcionPedidoViewSet(viewsets.ModelViewSet):
    queryset = RecepcionPedido.objects.all()
    serializer_class = RecepcionPedidoSerializer


class DetalleRecepcionViewSet(viewsets.ModelViewSet):
    queryset = DetalleRecepcion.objects.all()
    serializer_class = DetalleRecepcionSerializer


class CompraViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all()
    serializer_class = CompraSerializer

