from rest_framework import serializers
from .models import AlmacenOTienda, Inventario, TipoMovimiento, Movimiento
from productos.models import Producto
from usuarios.models import User

class AlmacenOTiendaSerializer(serializers.ModelSerializer):
    """Serializer para la tabla Almacenes y Tiendas."""
    
    class Meta:
        model = AlmacenOTienda
        fields = ['id_almacen_o_tienda', 'nombre']


class InventarioSerializer(serializers.ModelSerializer):
    """Serializer para la tabla Inventarios."""
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    almacen_o_tienda = serializers.PrimaryKeyRelatedField(queryset=AlmacenOTienda.objects.all())
    usuario_creacion = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    usuario_modificacion = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Inventario
        fields = ['id_inventario', 'producto', 'almacen_o_tienda', 'cantidad', 'stock_minimo',
                  'fecha_creacion', 'fecha_modificacion', 'usuario_creacion', 'usuario_modificacion', 'comentario_modificacion']

    def validate(self, data):
        """Validación de stock mínimo y cantidad."""
        if data.get('cantidad') < 0:
            raise serializers.ValidationError("La cantidad no puede ser negativa.")
        if data.get('stock_minimo') < 0:
            raise serializers.ValidationError("El stock mínimo no puede ser negativo.")
        return data


class TipoMovimientoSerializer(serializers.ModelSerializer):
    """Serializer para la tabla Tipo de Movimiento."""
    
    class Meta:
        model = TipoMovimiento
        fields = ['id_tipo', 'nombre', 'descripcion']


class MovimientoSerializer(serializers.ModelSerializer):
    """Serializer para la tabla Movimientos."""
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())
    origen = serializers.PrimaryKeyRelatedField(queryset=AlmacenOTienda.objects.all(), required=False)
    destino = serializers.PrimaryKeyRelatedField(queryset=AlmacenOTienda.objects.all(), required=False)
    tipo_movimiento = serializers.PrimaryKeyRelatedField(queryset=TipoMovimiento.objects.all())
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Movimiento
        fields = ['id_movimiento', 'producto', 'origen', 'destino', 'tipo_movimiento', 'cantidad', 
                  'fecha', 'usuario', 'fecha_creacion']

    def validate(self, data):
        """Validación de movimiento de productos."""
        if data.get('cantidad') < 0:
            raise serializers.ValidationError("La cantidad de movimiento no puede ser negativa.")
        
        if not data.get('origen') and not data.get('destino'):
            raise serializers.ValidationError("Debe haber al menos un origen o un destino para el movimiento.")
        
        # Verificar que no se haga un movimiento que deje el stock por debajo del mínimo
        if data.get('origen'):
            inventario_origen = Inventario.objects.filter(
                producto=data['producto'], almacen_o_tienda=data['origen']
            ).first()
            if inventario_origen and (inventario_origen.cantidad - data['cantidad'] < inventario_origen.stock_minimo):
                raise serializers.ValidationError(
                    f"No se puede realizar el movimiento. El stock en el origen no puede quedar por debajo del mínimo."
                )
        return data
