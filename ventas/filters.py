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

class VentasListFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr='gte')
    fecha_fin = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr='lte')
    cliente = django_filters.CharFilter(field_name="cliente__nombre", lookup_expr='icontains')
    tienda = django_filters.NumberFilter(field_name="tienda__id", lookup_expr='exact')
    metodo_pago = django_filters.CharFilter(field_name="metodo_pago", lookup_expr='icontains')

    class Meta:
        model = Venta
        fields = ['fecha_inicio', 'fecha_fin', 'cliente', 'tienda', 'metodo_pago']