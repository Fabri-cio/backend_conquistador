from rest_framework import serializers
from .models import Venta, DetalleVenta
from productos.models import Producto

# Serializer para el modelo DetalleVenta
class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['id_detalle', 'venta', 'producto', 'cantidad', 'precio_venta']

# Serializer para el modelo Venta
class VentaSerializer(serializers.ModelSerializer):
    # Serializa los detalles de la venta
    detalles = DetalleVentaSerializer(many=True, read_only=True)
    
    # Método para calcular el total de la venta en el serializer (solo lectura)
    total_venta = serializers.ReadOnlyField()

    class Meta:
        model = Venta
        fields = ['id_venta', 'fecha_venta', 'forma_pago', 'id_empleado', 'total_venta', 'detalles']

    def create(self, validated_data):
        # Crear la venta
        detalles_data = validated_data.pop('detalles')
        venta = Venta.objects.create(**validated_data)

        # Crear los detalles de la venta
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(venta=venta, **detalle_data)

        return venta

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        
        # Actualizar los campos de la venta
        instance.fecha_venta = validated_data.get('fecha_venta', instance.fecha_venta)
        instance.forma_pago = validated_data.get('forma_pago', instance.forma_pago)
        instance.id_empleado = validated_data.get('id_empleado', instance.id_empleado)
        instance.save()

        # Actualizar los detalles de la venta
        if detalles_data:
            for detalle_data in detalles_data:
                detalle = DetalleVenta.objects.get(id_detalle=detalle_data['id_detalle'])
                detalle.cantidad = detalle_data.get('cantidad', detalle.cantidad)
                detalle.precio_venta = detalle_data.get('precio_venta', detalle.precio_venta)
                detalle.save()

        return instance
