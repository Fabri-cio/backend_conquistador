from re import search
from rest_framework import viewsets
from .serializers import CategoriaSerializer, ProveedorSerializer, ProductoListSerializer, ProductoDetailSerializer, ProductoCreateSerializer, ProductosPorCategoriaSerializer, ProductosPorProveedorSerializer, ProductoHistorySerializer
from .models import Categoria, Proveedor, Producto
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductoFilter, CategoriaFilter
from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from core.views import AuditableModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser

class CategoriaView(PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()

    search_fields = [
        'nombre',
    ]

class ProveedorView(PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = ProveedorSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Proveedor.objects.all().order_by('id')

    search_fields = [
        'marca',
        'contacto',
        'telefono',
    ]

class ProductoView(PaginacionYAllDataMixin, AuditableModelViewSet):

    """
    Vista para gestionar productos con capacidades de búsqueda, filtrado, ordenamiento y paginación.

    Filtros personalizados (DjangoFilterBackend):
    - ?precio_min=10&precio_max=50 → Filtra productos dentro de un rango de precio
    - ?fecha_creacion_min=2024-01-01&fecha_creacion_max=2025-01-01 → Filtra por rango de fechas de creación
    - ?codigo_barras=1234567890123 → Búsqueda exacta por código de barras
    - ?categoria=2&proveedor=3 → Filtra por categoría y proveedor

    Búsqueda general (SearchFilter):
    - ?search=leche → Busca en campos texto relacionados (nombre, código barras, proveedor.marca, categoría.nombre)

    Ordenamiento (OrderingFilter):
    - ?ordering=precio → Ordena ascendente por precio
    - ?ordering=-fecha_creacion → Ordena descendente por fecha de creación

    Paginación:
    - ?page=1&per_page=10 → Control de paginación
    - ?all_data=true → Devuelve todos los productos sin paginar (útil para exportar)
    """
    queryset = Producto.objects.all()
    
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = ProductoFilter
    search_fields = [
        'nombre',
        'codigo_barras',
        'proveedor__marca',
        'categoria__nombre'
    ]
    ordering_fields = ['precio','fecha_creacion','nombre']
    ordering = ['-fecha_creacion']  # ✅ orden por defecto

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductoCreateSerializer
        return ProductoDetailSerializer
        
class ProductoHistoryView(generics.ListAPIView):
    serializer_class = ProductoHistorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        producto = get_object_or_404(Producto, pk=self.kwargs['pk'])
        return producto.history.all().order_by('-history_date')

class ProductoPorCategoriaView(generics.RetrieveAPIView):
    serializer_class = ProductosPorCategoriaSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Categoria.objects.all()

class ProductoPorProveedorView(generics.RetrieveAPIView):
    serializer_class = ProductosPorProveedorSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Proveedor.objects.all()
