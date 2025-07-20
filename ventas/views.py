# views.py
from rest_framework import viewsets
from .serializers import VentaSerializer, DetalleVentaSerializer, ClienteSerializer, FacturaVentaSerializer
from .models import Venta, DetalleVenta, Cliente, FacturaVenta
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import permissions

# Vista para el cliente
class ClienteView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('id_cliente')
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista para la factura de venta
class FacturaVentaView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = FacturaVenta.objects.all().order_by('id_factura')
    serializer_class = FacturaVentaSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista para la venta
class VentaView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('id_venta')
    serializer_class = VentaSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista para los detalles de la venta
class DetalleVentaView(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [permissions.IsAuthenticated]
