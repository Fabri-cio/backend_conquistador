# views.py
from django.db import models
from rest_framework import viewsets, permissions, filters   
from .serializers import PedidoSerializer, DetallePedidoSerializer, CompraSerializer, DetalleCompraSerializer, PedidoRecepcionSerializer, DetallesCompraPedidoSerializer, PedidoListSerializer, CompraListSerializer, CompraReporteSerializer
from .models import Pedido, DetallePedido, Compra, DetalleCompra
from django_crud_api.mixins import PaginacionYAllDataMixin
from core.views import AuditableModelViewSet
from core.mixins import FiltradoPorUsuarioInteligenteMixin
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PedidoFilter, CompraFilter

class PedidoRecepcionViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = Pedido.objects.all().order_by('id')
    serializer_class = PedidoRecepcionSerializer
    # permission_classes = [permissions.IsAuthenticated]

class PedidoViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
    queryset = Pedido.objects.all().order_by('id')
    serializer_class = PedidoSerializer
    # permission_classes = [permissions.IsAuthenticated]


class DetallePedidoViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = DetallePedido.objects.all().order_by('id')
    serializer_class = DetallePedidoSerializer
    permission_classes = [permissions.IsAuthenticated]


class CompraViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, AuditableModelViewSet):
    queryset = Compra.objects.all().order_by('id')
    serializer_class = CompraSerializer
    # permission_classes = [permissions.IsAuthenticated]


class DetalleCompraViewSet(PaginacionYAllDataMixin, viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.all().order_by('id')
    serializer_class = DetalleCompraSerializer
    permission_classes = [permissions.IsAuthenticated]

class DetallesCompraPedidoViewSet(viewsets.ModelViewSet):
    queryset = Compra.objects.all().order_by('id')
    serializer_class = DetallesCompraPedidoSerializer
    # permission_classes = [permissions.IsAuthenticated]

class PedidoListViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = PedidoListSerializer
    queryset = Pedido.objects.all()  # ✅ Esto evita el AssertionError

    # ✅ Filtros y búsqueda
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = PedidoFilter
    search_fields = ['proveedor__marca', 'almacen__nombre', 'observaciones']
    ordering_fields = ['fecha_creacion', 'fecha_entrega', 'estado']
    ordering = ['-fecha_creacion']  # orden por defecto

    def get_queryset(self):
        queryset = super().get_queryset()

        # Ultra rápido: solo trae los campos necesarios
        return queryset.select_related('proveedor', 'almacen').annotate(
            nombre_proveedor=models.F('proveedor__marca'),
            nombre_almacen=models.F('almacen__nombre')
        ).values(
            'id', 'estado', 'fecha_creacion', 'fecha_entrega', 'nombre_proveedor', 'nombre_almacen', 'observaciones'
        )
    # permission_classes = [permissions.IsAuthenticated]

class CompraListViewSet(FiltradoPorUsuarioInteligenteMixin, PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = CompraListSerializer
    queryset = Compra.objects.all()  # ✅ Esto evita el AssertionError

    # ✅ Filtros y búsqueda
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = CompraFilter
    search_fields = ['pedido__proveedor__marca', 'almacen__nombre']
    ordering_fields = ['fecha_creacion', 'fecha_entrega', 'estado']
    ordering = ['-fecha_creacion']  # orden por defecto

    def get_queryset(self):
        queryset = super().get_queryset()
        # Ultra rápido: solo trae los campos necesarios
        return queryset.select_related('almacen', 'pedido__proveedor').annotate(
            nombre_almacen=models.F('almacen__nombre'),
            nombre_proveedor=models.F('pedido__proveedor__marca')
        ).values(
            'id', 'fecha_creacion', 'nombre_proveedor', 'descuento', 'total_compra', 'nombre_almacen'
        )
    # permission_classes = [permissions.IsAuthenticated]

class CompraReporteViewSet(PaginacionYAllDataMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = CompraReporteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CompraFilter

    def get_queryset(self):
        return Compra.objects.values(
            'id', 
            'fecha_creacion', 
            'total_compra', 
            'almacen_id'  # DRF puede usar directamente
        ).order_by('-fecha_creacion')
