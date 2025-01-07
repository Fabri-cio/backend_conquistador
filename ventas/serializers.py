from rest_framework import serializers
from .models import Venta, DetalleVenta
from productos.models import Producto
from usuarios.models import CustomUser as User
from almacenes.models import Almacen

class DetalleVentaSerializer(serializers.ModelSerializer):
    id_producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    descuento_unitario = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        model = DetalleVenta
        fields = ['id_detalle_venta', 'id_venta', 'id_producto', 'cantidad', 'precio_unitario', 'subtotal', 'descuento_unitario']

    def validate(self, data):
        # Validación para asegurarse de que la cantidad sea positiva
        if data['cantidad'] <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor que cero.")
        return data

class VentaSerializer(serializers.ModelSerializer):
    id_usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    id_tienda = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
    detalles = DetalleVentaSerializer(many=True)

    class Meta:
        model = Venta
        fields = ['id_venta', 'fecha_venta', 'id_usuario', 'id_tienda', 'metodo_pago', 'descuento', 'total_venta', 'detalles']

    def create(self, validated_data):
        # Extraer los detalles de la venta
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)

        # Crear los detalles de la venta
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(id_venta=venta, **detalle_data)

        return venta

    def update(self, instance, validated_data):
        # Actualizar la venta con los nuevos datos
        detalles_data = validated_data.pop('detalles')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Eliminar los detalles existentes y crear los nuevos
        instance.detalles.all().delete()
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(id_venta=instance, **detalle_data)

        instance.save()
        return instance

    def validate(self, data):
        # Validación para asegurar que el descuento no sea mayor que el total de la venta
        if data.get('descuento', 0) > data.get('total_venta', 0):
            raise serializers.ValidationError("El descuento no puede ser mayor que el total de la venta.")
        return data
