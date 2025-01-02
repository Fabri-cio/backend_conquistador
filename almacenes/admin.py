from django.contrib import admin
from .models import AlmacenOTienda, Inventario, TipoMovimiento, Movimiento

# Personalización del admin para Inventario
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('producto', 'almacen_o_tienda', 'cantidad', 'stock_minimo', 'fecha_creacion', 'fecha_modificacion', 'usuario_creacion', 'usuario_modificacion')
    search_fields = ('producto__nombre', 'almacen_o_tienda__nombre')
    list_filter = ('almacen_o_tienda', 'producto', 'usuario_creacion', 'usuario_modificacion')
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    ordering = ('-fecha_creacion',)

class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'origen', 'destino', 'tipo_movimiento', 'cantidad', 'fecha', 'usuario', 'fecha_creacion')
    search_fields = ('producto__nombre', 'origen__nombre', 'destino__nombre', 'usuario__username')
    list_filter = ('tipo_movimiento', 'origen', 'destino', 'usuario')
    readonly_fields = ('fecha_creacion',)
    ordering = ('-fecha_creacion',)

# Registro de los modelos en el admin
admin.site.register(AlmacenOTienda)
admin.site.register(Inventario, InventarioAdmin)
admin.site.register(TipoMovimiento)
admin.site.register(Movimiento, MovimientoAdmin)
