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
        ]

class MovimientoSerializer(serializers.ModelSerializer):
    # Similar a los anteriores, definimos las relaciones a otras tablas
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    almacen = serializers.PrimaryKeyRelatedField(queryset=Almacen.objects.all())
    tipo = serializers.PrimaryKeyRelatedField(queryset=TipoMovimiento.objects.all())
    usuario_creacion = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

    nom_produc = serializers.CharField(source="producto.nombre", read_only=True)
    nom_alm = serializers.CharField(source="almacen.nombre", read_only=True)
    nom_tip = serializers.CharField(source="tipo.nombre", read_only=True)
    nom_user = serializers.CharField(source="usuario_creacion.email", read_only=True)

    class Meta:
        model = Movimiento
        fields = [
            'id',
            'cantidad',
            'fecha_creacion',
            'usuario_creacion',
            'nom_produc',
            'nom_alm',
            'nom_tip',
            'nom_user',
            'almacen',
            'producto',
            'tipo',
        ]