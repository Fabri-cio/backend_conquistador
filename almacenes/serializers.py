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
    id_producto_nombre = serializers.CharField(source="id_producto.nombre", read_only=True)
    precio = serializers.DecimalField(source="id_producto.precio", read_only=True, max_digits=10, decimal_places=2)
    id_almacen_tienda_nombre = serializers.CharField(source="id_almacen_tienda.nombre", read_only=True)
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
            'comentario_modificacion',
            'id_producto_nombre',
            'precio',
            'id_almacen_tienda_nombre',
        ]

class MovimientoSerializer(serializers.ModelSerializer):
    # Similar a los anteriores, definimos las relaciones a otras tablas
    id_producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    id_almacen = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
    id_tipo = serializers.PrimaryKeyRelatedField(queryset=TipoMovimiento.objects.all())
    id_usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    nom_produc = serializers.CharField(source="id_producto.nombre", read_only=True)
    nom_alm = serializers.CharField(source="id_almacen.nombre", read_only=True)
    nom_tip = serializers.CharField(source="id_tipo.nombre", read_only=True)
    nom_user = serializers.CharField(source="id_usuario.email", read_only=True)

    class Meta:
        model = Movimiento
        fields = [
            'id_movimiento',
            'id_producto',
            'id_almacen',
            'id_tipo',
            'cantidad',
            'fecha_creacion',
            'id_usuario',
            'fecha_creacion',
            'nom_produc',
            'nom_alm',
            'nom_tip',
            'nom_user',
        ]