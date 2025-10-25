from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Pedido, DetallePedido, Compra, DetalleCompra
from productos.mixins import ImageThumbMixinSerializer

class DetallePedidoRecepcionSerializer(ImageThumbMixinSerializer, serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.producto.nombre', read_only=True)
    cantidad_solicitada = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)
    imagen_url = serializers.SerializerMethodField()

    class Meta:
        model = DetallePedido
        fields = [
            'id',
            'producto',
            'cantidad_solicitada',
            'producto_nombre',
            'imagen_url'
        ]

    def get_imagen_url(self, obj):
        # reutiliza la miniatura del producto relacionado
        return self.get_image_url(obj, related_obj=obj.producto.producto)

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
    nombre_producto = serializers.CharField(source='producto.producto.nombre', read_only=True)
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
    nombre_producto = serializers.CharField(source="inventario.producto.nombre", read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DetalleCompra
        fields = ["id", "inventario", "cantidad", "precio_unitario", "descuento_unitario", "subtotal", "nombre_producto"]


class CompraSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True)
    almacen = serializers.PrimaryKeyRelatedField(read_only=True)
    nombre_proveedor = serializers.CharField(source="pedido.proveedor.marca", read_only=True)
    total_compra = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    # Totales calculados
    total_cantidad = serializers.SerializerMethodField()
    total_precio = serializers.SerializerMethodField()
    total_descuento = serializers.SerializerMethodField()
    total_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Compra
        fields = [
            "id", "pedido", "almacen", "nro_factura", "razon_social", "observaciones",
            "subtotal_compra", "descuento", "total_compra",
            "detalles", "nombre_proveedor",
            "total_cantidad", "total_precio", "total_descuento", "total_subtotal"
        ]

    def get_total_cantidad(self, obj):
        return sum([d.cantidad for d in obj.detalles.all()])

    def get_total_precio(self, obj):
        return sum([d.precio_unitario for d in obj.detalles.all()])

    def get_total_descuento(self, obj):
        return sum([d.descuento_unitario for d in obj.detalles.all()])

    def get_total_subtotal(self, obj):
        return sum([d.subtotal for d in obj.detalles.all()])

    def validate(self, data):
        pedido = data.get("pedido")
        if pedido and pedido.estado != "Pendiente":
            raise ValidationError("Solo se puede registrar compras de pedidos pendientes.")
        return data

    def create(self, validated_data):
        detalles_data = validated_data.pop("detalles")
        usuario = self.context["request"].user
        validated_data["almacen"] = usuario.lugar_de_trabajo

        with transaction.atomic():
            compra = Compra.objects.create(**validated_data)

            # Cambiar es estado de pedido de pendiente a recepcionado
            compra.pedido.estado = "Recepcionado"
            compra.pedido.save(update_fields=["estado"])

            for detalle_data in detalles_data:
                DetalleCompra.objects.create(compra=compra, **detalle_data)

        return compra

class DetallesCompraPedidoSerializer(serializers.ModelSerializer):
    detalles = DetalleCompraSerializer(many=True, read_only=True)
    detallesPedido = PedidoSerializer(source="pedido", read_only=True)
    almacen = serializers.PrimaryKeyRelatedField(read_only=True)
    nombre_proveedor = serializers.CharField(source="pedido.proveedor.marca", read_only=True)
    total_compra = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    # Totales calculados
    total_cantidad = serializers.SerializerMethodField()
    total_precio = serializers.SerializerMethodField()
    total_descuento = serializers.SerializerMethodField()
    total_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = Compra
        fields = [
            "id", "pedido", "almacen", "nro_factura", "razon_social", "observaciones",
            "subtotal_compra", "descuento", "total_compra",
            "detalles", "detallesPedido", "nombre_proveedor",
            "total_cantidad", "total_precio", "total_descuento", "total_subtotal"
        ]

    def get_total_cantidad(self, obj):
        return sum([d.cantidad for d in obj.detalles.all()])

    def get_total_precio(self, obj):
        return sum([d.precio_unitario for d in obj.detalles.all()])

    def get_total_descuento(self, obj):
        return sum([d.descuento_unitario for d in obj.detalles.all()])

    def get_total_subtotal(self, obj):
        return sum([d.subtotal for d in obj.detalles.all()])


class PedidoListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    estado = serializers.CharField()
    fecha_creacion = serializers.DateTimeField()
    fecha_entrega = serializers.DateField()
    nombre_proveedor = serializers.CharField()
    nombre_almacen = serializers.CharField()
    observaciones = serializers.CharField(allow_blank=True, allow_null=True)

class CompraListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fecha_creacion = serializers.DateTimeField()
    nombre_proveedor = serializers.CharField()
    descuento = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_compra = serializers.DecimalField(max_digits=12, decimal_places=2)
    nombre_almacen = serializers.CharField()

class CompraReporteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    almacen = serializers.IntegerField(source='almacen_id')
    fecha = serializers.DateTimeField(source="fecha_creacion", read_only=True)
    cantidad = serializers.DecimalField(source="total_compra", max_digits=10, decimal_places=2, read_only=True)