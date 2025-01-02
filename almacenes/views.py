from rest_framework import viewsets
from .models import AlmacenOTienda, Inventario, TipoMovimiento, Movimiento
from .serializer import AlmacenOTiendaSerializer, InventarioSerializer, TipoMovimientoSerializer, MovimientoSerializer

class AlmacenOTiendaViewSet(viewsets.ModelViewSet):
    queryset = AlmacenOTienda.objects.all()
    serializer_class = AlmacenOTiendaSerializer

class InventarioViewSet(viewsets.ModelViewSet):
    queryset = Inventario.objects.all()
    serializer_class = InventarioSerializer

class TipoMovimientoViewSet(viewsets.ModelViewSet):
    queryset = TipoMovimiento.objects.all()
    serializer_class = TipoMovimientoSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer
