from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Venta, DetalleVenta, Cliente, FacturaVenta
from almacenes.models import Inventario

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='id_inventario.id_producto.nombre', read_only=True)
    fecha_venta = serializers.DateTimeField(source='id_venta.fecha_venta', read_only=True)
    nombre_tienda = serializers.CharField(source='id_venta.id_tienda.nombre', read_only=True)

    class Meta:
        model = DetalleVenta
        fields = [
            'id_inventario',
            'nombre_producto',
            'nombre_tienda',
            'cantidad',
            'precio_unitario',
            'descuento_unitario',
            'subtotal',
            'fecha_venta',
        ]

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True)
    nombre_tienda = serializers.CharField(source='id_tienda.nombre', read_only=True)
    nom_user = serializers.CharField(source='id_usuario.get_full_name', read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id_venta',
            'fecha_venta',
            'id_usuario',
            'nom_user',
            'id_tienda',
            'nombre_tienda',
            'metodo_pago',
            'descuento',
            'total_venta',
            'detalles',
        ]

    # --- 3. Transacción atómica en create ---
    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        tienda_origen = validated_data.get('id_tienda')

        with transaction.atomic():
            venta = Venta.objects.create(**validated_data)

            for detalle_data in detalles_data:
                inventario = detalle_data.get('id_inventario')
                cantidad_vendida = detalle_data.get('cantidad')

                # Validar tienda
                if inventario.id_almacen_tienda != tienda_origen:
                    raise ValidationError(f"El inventario seleccionado no pertenece a la tienda {tienda_origen.nombre}.")

                # Validar stock suficiente
                if inventario.cantidad < cantidad_vendida:
                    raise ValidationError(
                        f"No hay suficiente stock para el producto {inventario.id_producto.nombre}. "
                        f"Disponible: {inventario.cantidad}."
                    )

                DetalleVenta.objects.create(id_venta=venta, **detalle_data)

        return venta

class FacturaVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaVenta
        fields = '__all__'
