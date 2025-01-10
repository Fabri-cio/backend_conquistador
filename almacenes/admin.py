from django.contrib import admin
from .models import Almacen, Inventario, Movimiento, TipoMovimiento

@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['id_producto', 'id_almacen_tienda', 'cantidad', 'stock_minimo', 'fecha_creacion', 'fecha_modificacion', 'usuario_creacion', 'usuario_modificacion', 'comentario_modificacion']
    search_fields = ['id_producto', 'id_almacen_tienda']
    list_filter = ['id_almacen_tienda', 'id_producto']
    
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'usuario_creacion', 'usuario_modificacion']

    fieldsets = (
        (None, {
            'fields': ('id_producto', 'id_almacen_tienda', 'cantidad', 'stock_minimo'),
        }),
        ('Información Adicional', {
            'fields': ('fecha_creacion', 'fecha_modificacion', 'usuario_creacion', 'usuario_modificacion', 'comentario_modificacion'),
            'classes': ('collapse',),
        }),
    ) 

    # Sobrescribe save_model para asignar automáticamente el usuario autenticado
    def save_model(self, request, obj, form, change):
        if not change or not obj.usuario_creacion:
            obj.usuario_creacion = request.user
        obj.usuario_modificacion = request.user
        super().save_model(request, obj, form, change)

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['id_producto', 'id_almacen', 'id_tipo', 'cantidad', 'get_id_usuario', 'fecha_creacion']
    search_fields = ['id_producto', 'id_almacen']
    list_filter = ['id_tipo', 'id_almacen']
    
    readonly_fields = ['id_usuario','fecha_creacion']

    fieldsets = (
        (None, {
            'fields': ('id_producto', 'id_almacen', 'id_tipo', 'cantidad'),
        }),
        ('Información Adicional', {
            'fields': ('id_usuario','fecha_creacion',),
            'classes': ('collapse',),
        }),
    )

    def get_id_usuario(self, obj):
        return obj.id_usuario.email if obj.id_usuario else "Sin usuario"
    get_id_usuario.short_description = "Usuario"

    # Sobrescribe save_model para asignar automáticamente el usuario autenticado
    def save_model(self, request, obj, form, change):
        if not change or not obj.id_usuario:
            obj.id_usuario = request.user
        super().save_model(request, obj, form, change)