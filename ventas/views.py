# views.py
from rest_framework import viewsets
from .serializers import VentaSerializer, DetalleVentaSerializer
from .models import Venta, DetalleVenta

# Vista para la venta
class VentaView(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

# Vista para los detalles de la venta
class DetalleVentaView(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
