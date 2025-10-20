from rest_framework import serializers
from .models import Almacen, TipoMovimiento, Inventario, Movimiento, Notificacion

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
    producto_barcode = serializers.CharField(source="producto.codigo_barras", read_only=True)
    imagen = serializers.ImageField(source="producto.imagen", read_only=True)

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
            'producto_barcode',
            'imagen',
        ]

class InventarioVentasSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source='producto.nombre', read_only=True)
    almacen_nombre = serializers.CharField(source='almacen.nombre', read_only=True)
    ventas = serializers.SerializerMethodField()

    class Meta:
        model = Inventario
        fields = [
            'id',
            'producto_nombre',
            'almacen_nombre',
            'cantidad',
            'stock_minimo',
            'stock_maximo',
            'ventas'
        ]

    def get_ventas(self, obj):
        # Detalles ya prefetch relacionados (solo 2 queries)
        detalles = getattr(obj, 'prefetched_ventas', obj.ventas.all())
        
        ventas_dict = {}
        for detalle in detalles:
            venta = detalle.venta
            if venta.id not in ventas_dict:
                ventas_dict[venta.id] = {
                    'id': venta.id,
                    'fecha_creacion': venta.fecha_creacion,
                    'cliente_nombre': venta.cliente.nombre if venta.cliente else None,
                    'total_venta': venta.total_venta,
                    'detalles': []
                }
            ventas_dict[venta.id]['detalles'].append({
                'cantidad': detalle.cantidad,
                'precio_unitario': detalle.precio_unitario,
                'sub_total': detalle.sub_total,
                'descuento_unitario': detalle.descuento_unitario
            })
        return list(ventas_dict.values())

class InventarioCarritoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="producto.nombre", read_only=True)
    precio = serializers.DecimalField(source="producto.precio", read_only=True, max_digits=10, decimal_places=2)
    producto_barcode = serializers.CharField(source="producto.codigo_barras", read_only=True)
    imagen = serializers.ImageField(source="producto.imagen", read_only=True)

    class Meta:
        model = Inventario  
        fields = [
            'id',
            'producto_nombre',
            'producto_barcode',
            'cantidad',
            'precio',
            'imagen',
        ]

# invetarioABC
class InventarioABCSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    producto_nombre = serializers.CharField()
    total_unidades = serializers.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_unidades = serializers.DecimalField(max_digits=5, decimal_places=2)
    acumulado_unidades = serializers.DecimalField(max_digits=5, decimal_places=2)
    categoria_unidades = serializers.CharField()
    
    total_valor = serializers.DecimalField(max_digits=12, decimal_places=2)
    porcentaje_valor = serializers.DecimalField(max_digits=5, decimal_places=2)
    acumulado_valor = serializers.DecimalField(max_digits=5, decimal_places=2)
    categoria_valor = serializers.CharField()

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

class NotificacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Notificacion
        fields = [
            'id',
            'usuario',
            'usuario_nombre',
            'titulo',
            'mensaje',
            'tipo',
            'leida',
            'inventario',
            'fecha_creacion',
            'fecha_modificacion',
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion', 'usuario_nombre']