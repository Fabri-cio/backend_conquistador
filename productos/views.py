from rest_framework import viewsets
from .serializers import CategoriaSerializer, ProveedorSerializer, ProductoSerializer, ProductosPorCategoriaSerializer, ProductosPorProveedorSerializer, ProductoHistorySerializer, CategoriaListSerializer, ProveedorListSerializer, ProductoListSerializer, CategoriaSelectSerializer, ProveedorSelectSerializer, ProveedorPedidosSerializer, ProductoSelectSerializer
from .models import Categoria, Proveedor, Producto
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductoFilter, CategoriaFilter, ProveedorFilter
from rest_framework import generics
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from core.views import AuditableModelViewSet
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

cache_alias = 'default'

# -------------------------------
# CRUD COMPLETO
# -------------------------------
class CategoriaView(PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = CategoriaSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = Categoria.objects.all().order_by('id')

class ProveedorView(PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = ProveedorSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = Proveedor.objects.all().order_by('id')

class ProductoView(PaginacionYAllDataMixin, AuditableModelViewSet):
    serializer_class = ProductoSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    queryset = Producto.objects.all().order_by('id')

# -------------------------------
# HISTORIAL
# -------------------------------
class ProductoHistoryView(generics.ListAPIView):
    serializer_class = ProductoHistorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        producto = get_object_or_404(Producto, pk=self.kwargs['pk'])
        return producto.history.all().order_by('-history_date')

# -------------------------------
# PRODUCTOS POR CATEGORIA / PROVEEDOR
# -------------------------------
class ProductoPorCategoriaView(generics.RetrieveAPIView):
    serializer_class = ProductosPorCategoriaSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Categoria.objects.all()

class ProductoPorProveedorView(generics.RetrieveAPIView):
    serializer_class = ProductosPorProveedorSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Proveedor.objects.all()

# -------------------------------
# LISTADOS CACHEADOS
# -------------------------------
@method_decorator(cache_page(60*5, cache=cache_alias), name='dispatch')  # Cachea 5 minutos
class CategoriaListView(PaginacionYAllDataMixin, generics.ListAPIView):
    serializer_class = CategoriaListSerializer
    # permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = CategoriaFilter
    search_fields = ['nombre']
    ordering_fields = ['estado', 'nombre']
    ordering = ['-estado']

    def get_queryset(self):
        # Solo traer los campos necesarios
        return Categoria.objects.only("id", "estado", "nombre", "imagen").order_by(*self.ordering)

@method_decorator(cache_page(60*5, cache=cache_alias), name='dispatch')  # Cachea 5 minutos
class ProveedorListView(PaginacionYAllDataMixin, generics.ListAPIView):
    serializer_class = ProveedorListSerializer
    # permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = ProveedorFilter
    search_fields = ['marca','contacto','telefono']
    ordering_fields = ['estado', 'marca','contacto','telefono']
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        # Solo traer los campos necesarios
        return Proveedor.objects.only("id", "estado", "marca", "contacto", "telefono", "imagen").order_by(*self.ordering)

# LISTA DE PRODUCTOS CACHE
@method_decorator(cache_page(60*5, cache=cache_alias), name='dispatch')  # Cachea 5 minutos
class ProductoListViewSet(PaginacionYAllDataMixin, generics.ListAPIView):
    serializer_class = ProductoListSerializer
    filter_backends = [
       DjangoFilterBackend,
       filters.SearchFilter,
       filters.OrderingFilter
    ]
    filterset_class = ProductoFilter
    search_fields = ['nombre', 'marca_proveedor','categoria_nombre']
    ordering_fields = ['precio','nombre']
    ordering = ['-nombre']  # ✅ orden por defecto

    def get_queryset(self):
        # Solo traer campos existentes y optimizar relaciones
        return (
            Producto.objects
            .select_related("proveedor", "categoria")
            .only("id", "estado", "nombre", "precio", "imagen", "proveedor__marca", "categoria__nombre")
            .order_by(*self.ordering)
        )

# -------------------------------
# SELECT / MINI LISTADOS
# -------------------------------
class CategoriaSelectViewSet(PaginacionYAllDataMixin, generics.ListAPIView):
    serializer_class = CategoriaSelectSerializer
    def get_queryset(self):
        return Categoria.objects.only("id", "nombre").order_by("nombre")

class ProveedorSelectViewSet(PaginacionYAllDataMixin, generics.ListAPIView):
    serializer_class = ProveedorSelectSerializer
    def get_queryset(self):
        return Proveedor.objects.only("id", "marca").order_by("marca")

class ProductoSelectViewSet(PaginacionYAllDataMixin, generics.ListAPIView):
    serializer_class = ProductoSelectSerializer
    def get_queryset(self):
        return Producto.objects.only("id", "nombre").order_by("nombre")

class ProveedorPedidosViewSet(PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ProveedorPedidosSerializer
    def get_queryset(self):
        return Proveedor.objects.only("id", "marca", "imagen").order_by("marca")

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