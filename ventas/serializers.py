# serializers.py
from django.forms import ValidationError
from rest_framework import serializers

from .models import Inventario
from .models import Venta, DetalleVenta

class DetalleVentaSerializer(serializers.ModelSerializer):
    # Obtener el nombre del producto desde el objeto relacionado Producto
    nombre_producto = serializers.CharField(source='id_producto.nombre', read_only=True)
    fecha_venta = serializers.DateTimeField(source='id_venta.fecha_venta', read_only=True)
    # Obtener el nombre de la tienda desde la relación de Venta
    nombre_tienda = serializers.CharField(source='id_venta.id_tienda.nombre', read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ['id_producto','nombre_producto','nombre_tienda', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal', 'fecha_venta']

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)
    nombre_tienda = serializers.CharField(source='id_tienda.nombre', read_only=True)  # Campo personalizado
    nom_user = serializers.CharField(source="id_usuario.get_full_name", read_only=True)


    class Meta:
        model = Venta
        fields = ['id_venta', 'fecha_venta', 'id_usuario','nom_user', 'id_tienda','nombre_tienda', 'metodo_pago', 'descuento', 'total_venta', 'detalles']

    def create(self, validated_data):
        # Extraer los datos de los detalles de venta
        detalles_data = validated_data.pop('detalles')
        venta = Venta(**validated_data)

        # Verificar el inventario antes de crear la venta y detalles
        for detalle_data in detalles_data:
            producto = detalle_data.get('id_producto')
            cantidad_vendida = detalle_data.get('cantidad')
            tienda_origen = validated_data.get('id_tienda')

            # Verificar si el producto tiene inventario en la tienda
            inventario = Inventario.objects.filter(id_producto=producto, id_almacen_tienda=tienda_origen).first()
            if not inventario:
                raise ValidationError(f"El producto {producto.nombre} no tiene inventario registrado en esta tienda.")
            
            if inventario.cantidad < cantidad_vendida:
                raise ValidationError(f"No hay suficiente stock para el producto {producto.nombre}.")

        # Si pasamos la verificación, se crea la venta
        venta.save()

        # Crear los detalles de venta y asociarlos a la venta
        for detalle_data in detalles_data:
            DetalleVenta.objects.create(id_venta=venta, **detalle_data)

        return venta