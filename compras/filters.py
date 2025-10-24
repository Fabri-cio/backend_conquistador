import django_filters
from .models import Pedido, Compra

class PedidoFilter(django_filters.FilterSet):
    fecha_creacion = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr="exact")
    fecha_entrega = django_filters.DateFilter(field_name="fecha_entrega", lookup_expr="exact")
    estado = django_filters.CharFilter(field_name="estado", lookup_expr="exact")
    
    class Meta:
        model = Pedido
        fields = []

class CompraFilter(django_filters.FilterSet):
    fecha_creacion = django_filters.DateFilter(field_name="fecha_creacion", lookup_expr="exact")
    
    class Meta:
        model = Compra
        fields = []
