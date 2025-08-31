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

    class Meta:
        model = DetalleVenta
        fields = ["inventario", "cantidad", "precio_unitario", "descuento_unitario", "sub_total"]

# Serializer para Venta
class VentaSerializer(serializers.ModelSerializer):
    total_venta = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ["id", "cliente", "usuario_creacion", "descuento", "quiere_comprobante", "total_venta", "detalles"]

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

# Serializer para ComprobanteVenta
class ComprobanteVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobanteVenta
        fields = '__all__'
