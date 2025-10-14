from rest_framework import viewsets
from .models import Almacen, TipoMovimiento, Inventario, Movimiento
from .serializers import AlmacenSerializer, TipoMovimientoSerializer, InventarioSerializer, MovimientoSerializer, InventarioCarritoSerializer, InventarioVentasSerializer, InventarioABCSerializer
from django_crud_api.mixins import PaginacionYAllDataMixin
from core.views import AuditableModelViewSet
from core.mixins import FiltradoPorUsuarioInteligenteMixin
from django.db.models import Prefetch
from ventas.models import DetalleVenta
from rest_framework import permissions
from django.db.models import Sum, F
from rest_framework.response import Response

class AlmacenViewSet(PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = AlmacenSerializer
    queryset = Almacen.objects.all().order_by('id')
    # permission_classes = [permissions.IsAuthenticated]

class TipoMovimientoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = TipoMovimientoSerializer
    queryset = TipoMovimiento.objects.all().order_by('id')

class InventarioViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all().order_by('id')
    # permission_classes = [permissions.IsAuthenticated]

class InventarioCarritoViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = InventarioCarritoSerializer
    queryset = Inventario.objects.all()

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

class InventarioABCViewSet(PaginacionYAllDataMixin, viewsets.GenericViewSet):
    """
    ABC por unidades (movimientos de salida) y por valor (ventas) optimizado.
    Solo dos queries a la base de datos.
    """
    serializer_class = InventarioABCSerializer
    queryset = []  # 👈 o Inventario.objects.none()

    def list(self, request):
        # 🔹 Consulta 1: Unidades (Movimientos de Salida)
        unidades_qs = Movimiento.objects.filter(tipo__naturaleza='Salida').values(
            'inventario__producto__id',
            'inventario__producto__nombre'
        ).annotate(total_unidades=Sum('cantidad')).order_by('-total_unidades')

        unidades_dict = {d['inventario__producto__id']: d for d in unidades_qs}
        total_unidades_global = sum([d['total_unidades'] for d in unidades_dict.values()]) or 1

        # Calcular porcentaje y acumulado para unidades
        acumulado_unidades = 0
        for d in unidades_dict.values():
            porcentaje = (d['total_unidades'] / total_unidades_global) * 100
            acumulado_unidades += porcentaje
            if acumulado_unidades <= 80:
                categoria = 'A'
            elif acumulado_unidades <= 95:
                categoria = 'B'
            else:
                categoria = 'C'
            d.update({
                'porcentaje_unidades': round(porcentaje, 2),
                'acumulado_unidades': round(acumulado_unidades, 2),
                'categoria_unidades': categoria
            })

        # 🔹 Consulta 2: Valor (Ventas)
        valor_qs = DetalleVenta.objects.values(
            'inventario__producto__id',
            'inventario__producto__nombre'
        ).annotate(total_valor=Sum(F('sub_total'))).order_by('-total_valor')

        valor_dict = {d['inventario__producto__id']: d for d in valor_qs}
        total_valor_global = sum([d['total_valor'] for d in valor_dict.values()]) or 1

        # Calcular porcentaje y acumulado para valor
        acumulado_valor = 0
        for d in valor_dict.values():
            porcentaje = (d['total_valor'] / total_valor_global) * 100
            acumulado_valor += porcentaje
            if acumulado_valor <= 80:
                categoria = 'A'
            elif acumulado_valor <= 95:
                categoria = 'B'
            else:
                categoria = 'C'
            d.update({
                'porcentaje_valor': round(porcentaje, 2),
                'acumulado_valor': round(acumulado_valor, 2),
                'categoria_valor': categoria
            })

        # 🔹 Combinar resultados
        final_result = []
        all_product_ids = set(list(unidades_dict.keys()) + list(valor_dict.keys()))

        for pid in all_product_ids:
            u = unidades_dict.get(pid, {
                'inventario__producto__nombre': valor_dict.get(pid, {}).get('inventario__producto__nombre', ''),
                'total_unidades': 0,
                'porcentaje_unidades': 0,
                'acumulado_unidades': 0,
                'categoria_unidades': 'C'
            })
            v = valor_dict.get(pid, {
                'total_valor': 0,
                'porcentaje_valor': 0,
                'acumulado_valor': 0,
                'categoria_valor': 'C'
            })
            final_result.append({
                'producto_id': pid,
                'producto_nombre': u['inventario__producto__nombre'],
                'total_unidades': u['total_unidades'],
                'porcentaje_unidades': u['porcentaje_unidades'],
                'acumulado_unidades': u['acumulado_unidades'],
                'categoria_unidades': u['categoria_unidades'],
                'total_valor': v['total_valor'],
                'porcentaje_valor': v['porcentaje_valor'],
                'acumulado_valor': v['acumulado_valor'],
                'categoria_valor': v['categoria_valor']
            })

        serializer = InventarioABCSerializer(final_result, many=True)
        return self.paginate_list(serializer.data, request)

class MovimientoViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = MovimientoSerializer 
    queryset = Movimiento.objects.all().order_by('id')
    # permission_classes = [permissions.IsAuthenticated]

    search_fields = [
        'tipo_nombre',
        'producto_nombre',
        'almacen_nombre',
        'usuario_creacion',
    ]

