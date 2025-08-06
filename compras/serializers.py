from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Pedido, DetallePedido, Compra, DetalleCompra

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'


class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = '__all__'

class DetalleCompraSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCompra
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True)
    class Meta:
        model = Compra
        fields = '__all__'

    def create(self, validated_data):
        # 1. Extraemos la lista de detalles (items de la compra) de los datos validados
        detalles_data = validated_data.pop('detalles')

        # 2. Obtenemos el almacén destino desde los datos validados (donde se almacenará la compra)
        almacen_origen = validated_data.get('almacen')

        # 3. Abrimos una transacción atómica para asegurar que todos los pasos se completen o ninguno
        with transaction.atomic():
            # 4. Creamos la compra con los datos restantes (sin detalles)
            compra = Compra.objects.create(**validated_data)

            # 5. Recorremos cada detalle en la lista
            for detalle_data in detalles_data:
                inventario = detalle_data.get('inventario')  # Objeto inventario relacionado
                cantidad_compra = detalle_data.get('cantidad')  # Cantidad comprada o recepcionada

            # 6. Validar que el inventario pertenece al almacén destino
            if inventario.almacen != almacen_origen:
                raise ValidationError(
                    f"El inventario seleccionado no pertenece al almacén {almacen_origen.nombre}."
                )

            # 7. Validar que la cantidad sea positiva (no se reciben cantidades negativas o cero)
            if cantidad_compra <= 0:
                raise ValidationError("La cantidad debe ser mayor que cero.")

            # 8. Validar que la cantidad recepcionada no exceda la cantidad pedida (opcional)
            # if cantidad_compra > detalle_data.get('cantidad_pedida', cantidad_compra):
            #     raise ValidationError("La cantidad recepcionada no puede exceder la cantidad pedida.")

            # 9. Crear el detalle de compra asociado a la compra recién creada
            DetalleCompra.objects.create(compra=compra, **detalle_data)

        # 10. Finalmente, devolver el objeto compra creado con sus detalles
        return compra






