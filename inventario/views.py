from rest_framework import viewsets
from .serializer import InventarioSerializer
from .models import Inventario

class InventarioView(viewsets.ModelViewSet):
    serializer_class = InventarioSerializer
    queryset = Inventario.objects.all()

