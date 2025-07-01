# views.py
from rest_framework import viewsets
from .serializers import VentaSerializer, DetalleVentaSerializer
from .models import Venta, DetalleVenta
from django_crud_api.mixins import PaginacionYAllDataMixin

# Vista para la venta
class VentaView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Venta.objects.all().order_by('id_venta')
    serializer_class = VentaSerializer

# Vista para los detalles de la venta
class DetalleVentaView(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
