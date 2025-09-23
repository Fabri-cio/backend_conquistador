import django_filters
from .models import Venta

class VentaReporteFilter(django_filters.FilterSet):
    fecha_inicio = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr='gte')
    fecha_fin = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr='lte')
    almacen = django_filters.CharFilter(field_name="tienda__nombre", lookup_expr='iexact')

    class Meta:
        model = Venta
        fields = []
