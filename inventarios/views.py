from rest_framework import viewsets
from .models import Almacen, TipoMovimiento, Inventario, Movimiento
from .serializers import AlmacenSerializer, TipoMovimientoSerializer, InventarioSerializer, MovimientoSerializer
from django_crud_api.mixins import PaginacionYAllDataMixin
from core.views import AuditableModelViewSet
from core.mixins import FiltradoPorUsuarioInteligenteMixin
from django.db.models import Prefetch
from ventas.models import DetalleVenta
from .serializers import InventarioVentasSerializer
from rest_framework import permissions

class AlmacenViewSet( PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = AlmacenSerializer
    queryset = Almacen.objects.all()

class TipoMovimientoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = TipoMovimientoSerializer
    queryset = TipoMovimiento.objects.all()

class InventarioViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all()
    permission_classes = [permissions.IsAuthenticated]

class InventarioVentasViewSet(PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = InventarioVentasSerializer

    queryset = Inventario.objects.select_related('producto', 'almacen').prefetch_related(
        Prefetch(
            'ventas',  # related_name en DetalleVenta
            queryset=DetalleVenta.objects.select_related(
                'venta',
                'venta__cliente',
                'inventario__producto',
                'inventario__almacen'
            ),
            to_attr='prefetched_ventas'  # prefetch con atributo para usar en get_ventas
        )
    )

class MovimientoViewSet(PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = MovimientoSerializer 
    queryset = Movimiento.objects.all()