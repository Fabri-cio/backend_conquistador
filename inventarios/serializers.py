from rest_framework import serializers
from .models import Almacen, TipoMovimiento, Inventario, Movimiento
from productos.models import Producto
from usuarios.models import Usuario

class AlmacenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Almacen
        fields = '__all__'

class TipoMovimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoMovimiento
        fields = '__all__'

class InventarioSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    precio = serializers.DecimalField(source="producto.precio", read_only=True, max_digits=10, decimal_places=2)
    almacen_nombre = serializers.CharField(source="almacen.nombre", read_only=True)


    class Meta:
        model = Inventario
        fields = [
            'id',
            'producto',
            'almacen',
            'cantidad',
            'stock_minimo',
            'stock_maximo',
            'fecha_creacion',
            'fecha_modificacion',
            'usuario_creacion',
            'usuario_modificacion',
            'comentario_modificacion',
            'producto_nombre',
            'precio',
            'almacen_nombre',
            'estado',
        ]

class MovimientoSerializer(serializers.ModelSerializer):
    tipo_nombre = serializers.CharField(source="tipo.nombre", read_only=True)
    producto_nombre = serializers.CharField(source="inventario.producto.nombre", read_only=True)
    almacen_nombre = serializers.CharField(source="inventario.almacen.nombre", read_only=True)
    usuario_creacion = serializers.CharField(source="usuario_creacion.username", read_only=True)

    class Meta:
        model = Movimiento
        fields = [
            'id',
            'inventario',
            'tipo_nombre',
            'tipo',
            'cantidad',
            'fecha_creacion',
            'fecha_modificacion',
            'usuario_creacion',
            'usuario_modificacion',
            'comentario_modificacion',
            'producto_nombre',
            'almacen_nombre',
            'usuario_creacion',
        ]