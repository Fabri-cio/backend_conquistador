import django_filters
from .models import Venta, DetalleVenta

class VentaReporteFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr='gte')
    fecha_fin = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr='lte')
    almacen = django_filters.NumberFilter(field_name="tienda__id", lookup_expr='exact')  # <-- aquí usamos NumberFilter

    class Meta:
        model = Venta
        fields = []

class VentasPorInventarioFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(field_name="venta__fecha_creacion", lookup_expr="gte")
    fecha_fin = django_filters.DateFilter(field_name="venta__fecha_creacion", lookup_expr="lte")
    inventario_id = django_filters.NumberFilter(field_name="inventario_id", lookup_expr="exact")

    class Meta:
        model = DetalleVenta
        fields = ['inventario_id', 'fecha_inicio', 'fecha_fin']