from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import CategoriaSerializer, ProveedorSerializer, ProductoSerializer
from .models import Categoria, Proveedor, Producto
from rest_framework.pagination import PageNumberPagination

# Definir una clase de paginación personalizada si quieres ajustar el tamaño de la página y el comportamiento
class PaginacionPersonalizada(PageNumberPagination):
    page_size = 10  # Número predeterminado de elementos por página
    page_size_query_param = 'page_size'  # Permitir cambiar el tamaño de la página desde los parámetros de la consulta
    max_page_size = 100  # Tamaño máximo de página permitido

class CategoriaView(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    queryset = Categoria.objects.all()

class ProveedorView(viewsets.ModelViewSet):
    serializer_class = ProveedorSerializer
    queryset = Proveedor.objects.all()

class ProductoView(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    queryset = Producto.objects.all().order_by('id_producto')  # Ordena por id_producto en lugar de id

    pagination_class = PaginacionPersonalizada

    def list(self, request, *args, **kwargs):
        all_data = request.query_params.get('all_data', 'false').lower() == 'true'  # Convierte a booleano correctamente

        if all_data:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

        return super().list(request, *args, **kwargs)  # Usa la paginación normal
