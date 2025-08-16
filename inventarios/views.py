from rest_framework import viewsets
from .models import Almacen, TipoMovimiento, Inventario, Movimiento
from .serializers import AlmacenSerializer, TipoMovimientoSerializer, InventarioSerializer, MovimientoSerializer
from django_crud_api.mixins import PaginacionYAllDataMixin
from core.views import AuditableModelViewSet
from django.db.models import Prefetch
from ventas.models import DetalleVenta
from .serializers import InventarioVentasSerializer

class AlmacenViewSet( PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = AlmacenSerializer
    queryset = Almacen.objects.all()

class TipoMovimientoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = TipoMovimientoSerializer
    queryset = TipoMovimiento.objects.all()

class InventarioViewSet(PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_superuser:
            return Inventario.objects.all().order_by('id')
        # Filtrar por lugar de trabajo solo si el usuario está autenticado y tiene un lugar de trabajo
        elif user.is_authenticated and user.lugar_de_trabajo:
            return Inventario.objects.filter(almacen=user.lugar_de_trabajo).order_by('id')
        return Inventario.objects.none()  # Si no tiene lugar de trabajo, no devuelve nada. O puedes devolver todo.

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