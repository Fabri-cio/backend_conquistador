import django_filters
from .models import Producto, Categoria, Proveedor

class ProductoFilter(django_filters.FilterSet):
    precio_min = django_filters.NumberFilter(field_name="precio", lookup_expr="gte")
    precio_max = django_filters.NumberFilter(field_name="precio", lookup_expr="lte")
    categoria = django_filters.CharFilter(field_name="categoria", lookup_expr="exact")
    proveedor = django_filters.CharFilter(field_name="proveedor", lookup_expr="exact")

    class Meta:
        model = Producto
        fields = []

class CategoriaFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name="nombre", lookup_expr="exact")

    class Meta:
        model = Categoria
        fields = []

class ProveedorFilter(django_filters.FilterSet):
    marca = django_filters.CharFilter(field_name="marca", lookup_expr="exact")

    class Meta:
        model = Proveedor
        fields = []

