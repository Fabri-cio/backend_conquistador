from rest_framework import serializers
from .models import Almacen, TipoMovimiento, Inventario, Movimiento, Producto, User

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = '__all__'

class TipoMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMovimiento
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    # Si quieres que el campo de producto sea más detallado, puedes usar un serializer para Producto
    id_producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    id_almacen_tienda = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
    usuario_creacion = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    usuario_modificacion = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Inventario
        fields = [
            'id_inventario',
            'id_producto',
            'id_almacen_tienda',
            'cantidad',
            'stock_minimo',
            'fecha_creacion',
            'fecha_modificacion',
            'usuario_creacion',
            'usuario_modificacion',
            'comentario_modificacion'
        ]

class MovimientoSerializer(serializers.ModelSerializer):
    # Similar a los anteriores, definimos las relaciones a otras tablas
    id_producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    id_almacen = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
    id_tipo = serializers.PrimaryKeyRelatedField(queryset=TipoMovimiento.objects.all())
    id_usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Movimiento
        fields = [
            'id_movimiento',
            'id_producto',
            'id_almacen',
            'id_tipo',
            'cantidad',
            'fecha',
            'id_usuario',
            'fecha_creacion'
        ]