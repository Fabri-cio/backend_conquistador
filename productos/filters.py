import django_filters
from .models import Producto

class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name="precio", lookup_expr="gte")
    precio_max = django_filters.NumberFilter(field_name="precio", lookup_expr="lte")
    fecha_creacion_min = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr="gte")
    fecha_creacion_max = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr="lte")
    codigo_barras = django_filters.CharFilter(field_name="codigo_barras", lookup_expr="exact")
    categoria = django_filters.CharFilter(field_name="categoria", lookup_expr="exact")
    proveedor = django_filters.CharFilter(field_name="proveedor", lookup_expr="exact")

    class Meta:
        model = Producto
        fields = []
