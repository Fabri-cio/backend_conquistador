from rest_framework import viewsets
from .serializer import ClienteSerializer, VentaSerializer, DetalleVentaSerializer
from .models import Cliente, Venta, DetalleVenta

class ClienteView(viewsets.ModelViewSet):
    serializer_class = ClienteSerializer
    queryset = Cliente.objects.all()
    
class VentaView(viewsets.ModelViewSet):
    serializer_class = VentaSerializer
    queryset = Venta.objects.all()
    
class DetalleVentaView(viewsets.ModelViewSet):
    serializer_class = DetalleVentaSerializer
    queryset = DetalleVenta.objects.all()