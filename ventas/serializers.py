from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Venta, DetalleVenta, Cliente, ComprobanteVenta

# Serializer para Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

# Serializer para DetalleVenta
class DetalleVentaSerializer(serializers.ModelSerializer):
    sub_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    nombre_producto = serializers.CharField(source="inventario.producto.nombre", read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ["inventario", "cantidad", "precio_unitario", "descuento_unitario", "sub_total", "nombre_producto"]

# Serializer para Venta
class VentaSerializer(serializers.ModelSerializer):
    fecha_creacion = serializers.DateTimeField(read_only=True)
    usuario_creacion = serializers.CharField(source="usuario_creacion.username", read_only=True)
    nombre_tienda = serializers.CharField(source="tienda.nombre", read_only=True)
    total_venta = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    detalles = DetalleVentaSerializer(many=True)

    # NUEVOS CAMPOS DE TOTALES
    total_cantidad = serializers.SerializerMethodField()
    total_precio = serializers.SerializerMethodField()
    total_descuento = serializers.SerializerMethodField()
    total_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Venta
        fields = [
            "id", "cliente", "usuario_creacion", "descuento", "quiere_comprobante", 
            "total_venta", "detalles", "fecha_creacion", "nombre_tienda", "metodo_pago",
            "total_cantidad", "total_precio", "total_descuento", "total_subtotal"]

    # mandamos a react totales ya calculados
    def get_total_cantidad(self, obj):
        return sum([d.cantidad for d in obj.detalles.all()])

    def get_total_precio(self, obj):
        return sum([d.precio_unitario for d in obj.detalles.all()])

    def get_total_descuento(self, obj):
        return sum([d.descuento_unitario for d in obj.detalles.all()])

    def get_total_subtotal(self, obj):
        return sum([d.sub_total for d in obj.detalles.all()])

    # Validaciones a nivel de serializer
    def validate(self, attrs):
        if attrs.get("quiere_comprobante") and not attrs.get("cliente"):
            raise serializers.ValidationError("Debe seleccionar un cliente si se requiere comprobante.")
        if attrs.get("cliente") and not attrs.get("quiere_comprobante"):
            raise serializers.ValidationError("No puede asignar cliente si no se requiere comprobante.")
        return attrs

    # Sobrescribimos create para manejar detalles dentro de transacción
    def create(self, validated_data):
        detalles_data = validated_data.pop("detalles")

        # Setear la tienda desde el usuario logueado
        usuario = self.context['request'].user
        validated_data['tienda'] = usuario.lugar_de_trabajo

        with transaction.atomic():
            venta = Venta.objects.create(**validated_data)
            for detalle_data in detalles_data:
                DetalleVenta.objects.create(venta=venta, **detalle_data)
        return venta

class VentaReporteSerializer(serializers.ModelSerializer):
    fecha = serializers.DateTimeField(source="fecha_creacion", read_only=True)
    almacen = serializers.CharField(source="tienda.nombre", read_only=True)
    total_venta = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Venta
        fields = ["fecha", "almacen", "total_venta"]

# Serializer para ComprobanteVenta
class ComprobanteVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobanteVenta
        fields = '__all__'
