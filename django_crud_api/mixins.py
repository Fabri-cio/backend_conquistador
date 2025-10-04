from rest_framework import status
from rest_framework.response import Response
from .pagination import PaginacionPersonalizada

class PaginacionYAllDataMixin:
    pagination_class = PaginacionPersonalizada  # Esto se aplica directamente a las vistas que usen este mixin

    def list(self, request, *args, **kwargs):
        # Maneja el parámetro 'all_data' para obtener todos los elementos sin paginación
        all_data = request.query_params.get('all_data', 'false').lower() == 'true'

        if all_data:
             # ✅ Aplica filtros, búsqueda y ordenamiento
            queryset = self.filter_queryset(self.get_queryset())
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Si no es 'all_data', utiliza la paginación normal
        return super().list(request, *args, **kwargs)

     # 🔑 Nuevo helper para listas calculadas (como InventarioABC)
    def paginate_list(self, data, request):
        all_data = request.query_params.get('all_data', 'false').lower() == 'true'
        if all_data:
            return Response(data, status=status.HTTP_200_OK)

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(data, request, view=self)
        if page is not None:
            return paginator.get_paginated_response(page)

        return Response(data, status=status.HTTP_200_OK)
