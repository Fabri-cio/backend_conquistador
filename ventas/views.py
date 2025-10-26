# views.py
from rest_framework import viewsets
from .serializers import VentaSerializer, DetalleVentaSerializer, ClienteSerializer, ComprobanteVentaSerializer, VentaReporteSerializer, VentaListSerializer
from .models import Venta, DetalleVenta, Cliente, ComprobanteVenta
from django_crud_api.mixins import PaginacionYAllDataMixin
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from core.views import AuditableModelViewSet
from rest_framework import filters
from .filters import VentaReporteFilter, VentasPorInventarioFilter, VentasListFilter
from django_filters.rest_framework import DjangoFilterBackend
from core.mixins import FiltradoPorUsuarioInteligenteMixin
from ventas.services_ventas_por_inventario import obtener_ventas_por_inventario
from django.core.cache import cache
from django.db.models import F
from django.db import models

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
    search_fields = [
        'numero_comprobante'
    ]

# Vista para la venta
class VentaView(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
    queryset = (
        Venta.objects
        .select_related("cliente", "tienda")
        .prefetch_related("detalles__inventario__producto")
        .all()
        .order_by("id")
    )
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
    queryset = DetalleVenta.objects.select_related("inventario__producto").all().order_by("id")
    serializer_class = DetalleVentaSerializer
    # permission_classes = [permissions.IsAuthenticated]

class VentasPorInventarioViewSet(PaginacionYAllDataMixin, viewsets.ViewSet):
    """
    Endpoint para obtener ventas por inventario y por rango de fechas con paginación.
    """
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VentasPorInventarioFilter

    def list(self, request):
        # Aplicamos filtros
        filterset = self.filterset_class(request.GET, queryset=None)
        if not filterset.is_valid():
            return Response(filterset.errors, status=400)

        inventario_id = filterset.form.cleaned_data.get('inventario_id')
        fecha_inicio = filterset.form.cleaned_data.get('fecha_inicio')
        fecha_fin = filterset.form.cleaned_data.get('fecha_fin')

        if not inventario_id:
            return Response({"error": "Falta inventario_id"}, status=400)

        datos = obtener_ventas_por_inventario(inventario_id, fecha_inicio, fecha_fin)

        # Usamos la función de paginación del mixin
        return self.paginate_list(datos, request)

class VentaListViewSet(PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = VentaListSerializer
    queryset = Venta.objects.all()  # Necesario para evitar AssertionError

    # Filtros, búsqueda y orden
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = VentasListFilter
    search_fields = ['cliente__nombre', 'tienda__nombre', 'metodo_pago']
    ordering_fields = ['fecha_creacion', 'total_venta']
    ordering = ['-fecha_creacion']  # orden por defecto

    def get_queryset(self):
        """
        Devuelve solo los campos necesarios, ultrarrápido y compatible con filtros, búsqueda y paginación.
        """
        queryset = super().get_queryset()  # aplica FiltradoPorUsuarioInteligenteMixin

        return queryset.select_related('cliente', 'tienda', 'usuario_creacion').annotate(
            nombre_cliente=models.F('cliente__nombre'),
            nombre_tienda=models.F('tienda__nombre'),
            nombre_cajero=models.F('usuario_creacion__username')
        ).values(
            'id',
            'fecha_creacion',
            'nombre_cliente',
            'nombre_tienda',
            'nombre_cajero',
            'metodo_pago',
            'descuento',
            'total_venta'
        ).order_by('-fecha_creacion')


# Vista para reporte de ventas
class VentaReporteView(PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = VentaReporteSerializer
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VentaReporteFilter
    
    def get_queryset(self):
        return Venta.objects.select_related('tienda').only(
            "id", "fecha_creacion", "total_venta", "tienda__id"
        ).order_by("fecha_creacion")