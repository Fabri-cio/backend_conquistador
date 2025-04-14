from rest_framework import viewsets
from .serializer import CategoriaSerializer, ProveedorSerializer, ProductoSerializer
from .models import Categoria, Proveedor, Producto
from django_crud_api.mixins import PaginacionYAllDataMixin

class CategoriaView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all().order_by('id_categoria')

class ProveedorView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all().order_by('id_proveedor')

class ProductoView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all().order_by('id_producto')