import django_filters
from .models import Producto, Categoria, Proveedor

class ProductoListFilter(django_filters.FilterSet):

    class Meta:
        model = Producto
        fields = []

class CategoriaListFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name="nombre", lookup_expr="exact")

    class Meta:
        model = Categoria
        fields = []

class ProveedorListFilter(django_filters.FilterSet):
    marca = django_filters.CharFilter(field_name="marca", lookup_expr="exact")

    class Meta:
        model = Proveedor
        fields = []

