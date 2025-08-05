from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Venta, DetalleVenta, Cliente, ComprobanteVenta
from inventarios.models import Inventario

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    nombre_producto = serializers.CharField(source='id_inventario.id_producto.nombre', read_only=True)
    fecha_venta = serializers.DateTimeField(source='id_venta.fecha_creacion', read_only=True)
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
    usuario_creacion = serializers.CharField(source='usuario_creacion.first_name', read_only=True)

    class Meta:
        model = Venta
        fields = [
            'id_venta',
            'fecha_creacion',
            'usuario_creacion',
            'id_tienda',
            'nombre_tienda',
            'metodo_pago',
            'descuento',
            'total_venta',
            'detalles',
        ]

    # --- 3. Transacción atómica en create ---
    def create(self, validated_data):
        # 1. Se extrae la lista de detalles (items de venta) de los datos validados
        detalles_data = validated_data.pop('detalles')

        # 2. Se obtiene la tienda origen desde los datos validados (donde se realiza la venta)
        tienda_origen = validated_data.get('id_tienda')

        # 3. Se abre una transacción atómica para asegurar que todos los pasos se completen o ninguno
        with transaction.atomic():

            # 4. Se crea la venta con los datos restantes (sin detalles)
            venta = Venta.objects.create(**validated_data)

            # 5. Por cada detalle en la lista
            for detalle_data in detalles_data:
                inventario = detalle_data.get('id_inventario')
                cantidad_vendida = detalle_data.get('cantidad')

                # 6. Validar que el inventario pertenece a la tienda origen
                if inventario.id_almacen_tienda != tienda_origen:
                    raise ValidationError(f"El inventario seleccionado no pertenece a la tienda {tienda_origen.nombre}.")

                # 7. Validar que el stock disponible sea suficiente para la cantidad vendida
                if inventario.cantidad < cantidad_vendida:
                    raise ValidationError(
                        f"No hay suficiente stock para el producto {inventario.id_producto.nombre}. "
                        f"Disponible: {inventario.cantidad}."
                    )

                # 8. Crear el detalle de venta asociado a la venta recién creada
                DetalleVenta.objects.create(id_venta=venta, **detalle_data)

        # 9. Finalmente, devuelve el objeto venta creado con sus detalles
        return venta

class ComprobanteVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComprobanteVenta
        fields = '__all__'
