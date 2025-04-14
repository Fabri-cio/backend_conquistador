from rest_framework import viewsets
from .models import Almacen, TipoMovimiento, Inventario, Movimiento
from .serializers import AlmacenSerializer, TipoMovimientoSerializer, InventarioSerializer, MovimientoSerializer
from django_crud_api.mixins import PaginacionYAllDataMixin

class AlmacenViewSet( PaginacionYAllDataMixin,viewsets.ModelViewSet):
    serializer_class = AlmacenSerializer
    queryset = Almacen.objects.all().order_by('id_almacen_tienda')

class TipoMovimientoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = TipoMovimientoSerializer
    queryset = TipoMovimiento.objects.all().order_by('id_tipo')

class InventarioViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all().order_by('id_inventario')

class MovimientoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer 
    queryset = Movimiento.objects.all().order_by('id_movimiento')