# views.py
from rest_framework import viewsets
from .serializers import VentaSerializer, DetalleVentaSerializer, ClienteSerializer, ComprobanteVentaSerializer
from .models import Venta, DetalleVenta, Cliente, ComprobanteVenta
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from core.views import AuditableModelViewSet

# Vista para el cliente
class ClienteView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer
    # permission_classes = [permissions.IsAuthenticated]

# Vista para la factura de venta
class ComprobanteVentaView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = ComprobanteVenta.objects.all().order_by('id')
    serializer_class = ComprobanteVentaSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista para la venta
class VentaView(PaginacionYAllDataMixin, AuditableModelViewSet):
    queryset = Venta.objects.all().order_by('id')
    serializer_class = VentaSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("Payload recibido en backend:", request.data)  # <-- Aquí ves el JSON real
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# Vista para los detalles de la venta
class DetalleVentaView(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all().order_by('id')
    serializer_class = DetalleVentaSerializer
    # permission_classes = [permissions.IsAuthenticated]
