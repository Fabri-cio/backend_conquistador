from rest_framework import viewsets
from .serializer import CategoriaSerializer, ProveedorSerializer, ProductoListSerializer, ProductoDetailSerializer, ProductoCreateSerializer
from .models import Categoria, Proveedor, Producto
from django_crud_api.mixins import PaginacionYAllDataMixin

class CategoriaView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all().order_by('id_categoria')

class ProveedorView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all().order_by('id_proveedor')

class ProductoView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('id_producto')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductoListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductoCreateSerializer
        return ProductoDetailSerializer