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

    # def get_queryset(self):
    #     user = self.request.user
    #     # Filtrar por lugar de trabajo solo si el usuario está autenticado y tiene un lugar de trabajo
    #     if user.is_authenticated and user.lugar_de_trabajo:
    #         return Inventario.objects.filter(id_almacen_tienda=user.lugar_de_trabajo).order_by('id_inventario')
    #     return Inventario.objects.none()  # Si no tiene lugar de trabajo, no devuelve nada. O puedes devolver todo.


class MovimientoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = MovimientoSerializer 
    queryset = Movimiento.objects.all().order_by('id_movimiento')