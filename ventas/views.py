from rest_framework import viewsets
from .models import Venta, DetalleVenta
from .serializer import VentaSerializer, DetalleVentaSerializer
from rest_framework.permissions import IsAuthenticated  # Si necesitas autenticación

# ViewSet para el modelo Venta
class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()  # Obtener todas las ventas
    serializer_class = VentaSerializer  # Usar el serializador de la venta
    # permission_classes = [IsAuthenticated]  # Si necesitas autenticar a los usuarios

    def perform_create(self, serializer):
        # Si deseas realizar alguna acción adicional al crear una venta, puedes hacerlo aquí
        # Por ejemplo, manejar el cálculo del total o cualquier validación extra
        serializer.save()  # Guarda la venta

# ViewSet para el modelo DetalleVenta
class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()  # Obtener todos los detalles de la venta
    serializer_class = DetalleVentaSerializer  # Usar el serializador de detalle de venta
    # permission_classes = [IsAuthenticated]  # Si necesitas autenticar a los usuarios
