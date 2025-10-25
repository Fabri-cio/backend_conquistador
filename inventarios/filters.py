import django_filters
from .models import Inventario

class InventarioReporteFilter(django_filters.FilterSet):
    # 🔹 Permite filtrar por producto (nombre parcial o completo)
    producto__nombre = django_filters.CharFilter(
        field_name='producto__nombre', lookup_expr='icontains', label='Producto'
    )

    # 🔹 Permite filtrar por almacén (por ID exacto)
    almacen = django_filters.NumberFilter(
        field_name='almacen', lookup_expr='exact', label='Almacén'
    )

    # 🔹 Permite filtrar por estado (True / False)
    estado = django_filters.BooleanFilter(
        field_name='estado', lookup_expr='exact', label='Activo'
    )

    class Meta:
        model = Inventario
        fields = [
            'producto__nombre',
            'almacen',
            'estado',
        ]
