from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Venta, DetalleVenta
from .serializers import VentaSerializer, DetalleVentaSerializer
from rest_framework.permissions import IsAuthenticated

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]

    # Acción personalizada para obtener detalles de una venta específica
    @action(detail=True, methods=['get'])
    def detalles(self, request, pk=None):
        venta = self.get_object()
        detalles = venta.detalles.all()
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # Aquí podrías agregar lógica adicional si necesitas
        serializer.save(id_usuario=self.request.user)

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Aquí podrías agregar lógica adicional si necesitas
        serializer.save()
