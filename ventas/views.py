# views.py
from rest_framework import viewsets
from .serializers import VentaSerializer, DetalleVentaSerializer, ClienteSerializer, ComprobanteVentaSerializer, VentaReporteSerializer
from .models import Venta, DetalleVenta, Cliente, ComprobanteVenta
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from core.views import AuditableModelViewSet
from rest_framework import filters
from .filters import VentaReporteFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.mixins import FiltradoPorUsuarioInteligenteMixin

# Vista para el cliente
class ClienteView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer

    # activar busqueda
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'nombre',
        'correo',
        'nit_ci'
    ]
    # permission_classes = [permissions.IsAuthenticated]

# Vista para la factura de venta
class ComprobanteVentaView(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = ComprobanteVenta.objects.all().order_by('id')
    serializer_class = ComprobanteVentaSerializer
    permission_classes = [permissions.IsAuthenticated]

# Vista para la venta
class VentaView(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
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

# Vista para reporte de ventas
class VentaReporteView(PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaReporteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VentaReporteFilter

# Vista para los detalles de la venta
class DetalleVentaView(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all().order_by('id')
    serializer_class = DetalleVentaSerializer
    # permission_classes = [permissions.IsAuthenticated]
