from rest_framework import viewsets
from .serializer import ProveedorSerializer, OrdenCompraSerializer, DetalleOrdenSerializer
from .models import Proveedor, OrdenCompra, DetalleOrden

class ProveedorView(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()
    
class OrdenCompraView(viewsets.ModelViewSet):
    serializer_class = OrdenCompraSerializer
    queryset = OrdenCompra.objects.all()
    
class DetalleOrdenView(viewsets.ModelViewSet):
    serializer_class = DetalleOrdenSerializer
    queryset = DetalleOrden.objects.all()