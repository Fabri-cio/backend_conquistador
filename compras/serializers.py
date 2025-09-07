from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Pedido, DetallePedido, Compra, DetalleCompra

class DetallePedidoRecepcionSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.producto.nombre', read_only=True)
    producto_imagen = serializers.ImageField(source='producto.producto.imagen', read_only=True)
    cantidad_solicitada = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)

    class Meta:
        model = DetallePedido
        fields = [
            'id',
            'producto',
            'cantidad_solicitada',
            'producto_nombre',
            'producto_imagen'
        ]

class PedidoRecepcionSerializer(serializers.ModelSerializer):
    nombre_proveedor = serializers.CharField(source='proveedor.marca', read_only=True)
    imagen_proveedor = serializers.ImageField(source='proveedor.imagen', read_only=True)
    detalles = DetallePedidoRecepcionSerializer(many=True, read_only=True)

    class Meta:
        model = Pedido
        fields = [
            'id',
            'proveedor', 
            'fecha_entrega', 
            'observaciones', 
            'detalles', 
            'nombre_proveedor',
            'imagen_proveedor'
        ]

class DetallePedidoSerializer(serializers.ModelSerializer):
    pedido = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = DetallePedido
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    nombre_proveedor = serializers.CharField(source='proveedor.marca', read_only=True)
    almacen = serializers.PrimaryKeyRelatedField(read_only=True) #aqui el almacen es solo de lectura y no manda react
    nombre_almacen = serializers.CharField(source='almacen.nombre', read_only=True)
    detalles = DetallePedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = '__all__'

    def validate_detalles(self, detalles):
        if not detalles:
            raise ValidationError("Debe incluir al menos un detalle de pedido.")

        for idx, detalle in enumerate(detalles, start=1):
            producto = detalle.get('producto')
            cantidad = detalle.get('cantidad_solicitada')

            if producto is None:
                raise ValidationError({f"detalle_{idx}": "El producto es obligatorio."})

            if cantidad is None or cantidad <= 0:
                raise ValidationError({f"detalle_{idx}": "La cantidad solicitada debe ser mayor que cero."})

        return detalles

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')

        usuario = self.context['request'].user
        validated_data['almacen'] = usuario.lugar_de_trabajo

        with transaction.atomic():
            pedido = Pedido.objects.create(**validated_data)

            for idx, detalle_data in enumerate(detalles_data, start=1):
                producto = detalle_data.get('producto')

                # Validación extra opcional: si quieres verificar que el inventario está activo
                if not producto.estado:
                    raise ValidationError({f"detalle_{idx}": "El inventario no está disponible para pedidos."})

            detalles_objs = [
                DetallePedido(pedido=pedido, **detalle_data)
                for detalle_data in detalles_data
            ]
            DetallePedido.objects.bulk_create(detalles_objs)

        return pedido

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)

        with transaction.atomic():
            # Actualizar campos simples del pedido
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if detalles_data is not None:
                # Mapear detalles existentes por id para actualización
                detalles_actuales = {detalle.id: detalle for detalle in instance.detalles.all()}

                nuevos_detalles = []

                for detalle_data in detalles_data:
                    detalle_id = detalle_data.get('id', None)

                    # Validar inventario activo
                    producto = detalle_data.get('producto')
                    if not producto.estado:
                        raise ValidationError("El inventario no está disponible para pedidos.")

                    if detalle_id and detalle_id in detalles_actuales:
                        # Actualizar detalle existente
                        detalle_obj = detalles_actuales.pop(detalle_id)
                        for attr, value in detalle_data.items():
                            setattr(detalle_obj, attr, value)
                        detalle_obj.save()
                    else:
                        # Nuevo detalle a crear luego
                        nuevos_detalles.append(detalle_data)

                # Los que quedan en detalles_actuales no fueron enviados en el update -> eliminarlos
                for detalle_obj in detalles_actuales.values():
                    detalle_obj.delete()

                # Crear nuevos detalles
                detalles_objs = [
                    DetallePedido(pedido=instance, **detalle_data)
                    for detalle_data in nuevos_detalles
                ]
                DetallePedido.objects.bulk_create(detalles_objs)

        return instance

class DetalleCompraSerializer(serializers.ModelSerializer):
    compra = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = DetalleCompra
        fields = '__all__'

class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True)

    nombre_proveedor = serializers.CharField(source='pedido.proveedor.marca', read_only=True)

    class Meta:
        model = Compra
        fields = '__all__'

    def validate_detalles(self, detalles):
        if not detalles:
            raise ValidationError("Debe incluir al menos un detalle de compra.")
        return detalles

    def validate(self, data):
        detalles = data.get('detalles', [])

        for idx, detalle in enumerate(detalles, start=1):
            inventario = detalle.get('inventario')
            cantidad = detalle.get('cantidad')
            precio_unitario = detalle.get('precio_unitario')
            descuento_unitario = detalle.get('descuento_unitario')

            if inventario is None:
                raise ValidationError({f"detalle_{idx}": "El inventario es obligatorio."})

            if cantidad is None or cantidad <= 0:
                raise ValidationError({f"detalle_{idx}": "La cantidad debe ser mayor que cero."})

            if precio_unitario is None or precio_unitario < 0:
                raise ValidationError({f"detalle_{idx}": "El precio unitario debe ser mayor o igual a cero."})

            if descuento_unitario is None or descuento_unitario < 0:
                raise ValidationError({f"detalle_{idx}": "El descuento unitario no puede ser negativo."})

            subtotal = (cantidad * precio_unitario) - descuento_unitario
            if subtotal < 0:
                raise ValidationError({f"detalle_{idx}": "El subtotal no puede ser negativo."})

            if descuento_unitario > (cantidad * precio_unitario):
                raise ValidationError({f"detalle_{idx}": "El descuento unitario no puede ser mayor que el subtotal parcial."})

        return data

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalles')
        with transaction.atomic():
            compra = Compra.objects.create(**validated_data)
            detalles_objs = [DetalleCompra(compra=compra, **detalle) for detalle in detalles_data]
            DetalleCompra.objects.bulk_create(detalles_objs)
        return compra

    def update(self, instance, validated_data):
        detalles_data = validated_data.pop('detalles', None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            if detalles_data is not None:
                detalles_actuales = {d.id: d for d in instance.detalles.all()}
                nuevos_detalles = []

                for detalle_data in detalles_data:
                    detalle_id = detalle_data.get('id')
                    if detalle_id and detalle_id in detalles_actuales:
                        detalle_obj = detalles_actuales.pop(detalle_id)
                        for attr, value in detalle_data.items():
                            setattr(detalle_obj, attr, value)
                        detalle_obj.save()
                    else:
                        nuevos_detalles.append(detalle_data)

                for detalle_obj in detalles_actuales.values():
                    detalle_obj.delete()

                detalles_objs = [DetalleCompra(compra=instance, **d) for d in nuevos_detalles]
                DetalleCompra.objects.bulk_create(detalles_objs)

        return instance




