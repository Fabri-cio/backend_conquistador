from rest_framework import viewsets
from .serializer import CategoriaSerializer, ProductoSerializer
from .models import Categoria, Producto

class ProductoView(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all()

class CategoriaView(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()

