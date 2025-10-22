from django.contrib import admin
from .models import Almacen, Inventario, Movimiento, TipoMovimiento, Notificacion

@admin.register(Almacen)
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    search_fields = ['nombre']

    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'usuario_creacion', 'usuario_modificacion','comentario_modificacion']

@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'almacen', 'producto', 'cantidad', 'stock_minimo', 'stock_maximo', 'fecha_creacion', 'fecha_modificacion', 'usuario_creacion', 'usuario_modificacion', 'comentario_modificacion']
    search_fields = ['producto', 'almacen']
    list_filter = ['almacen', 'producto']
    
    readonly_fields = ['fecha_creacion', 'fecha_modificacion', 'usuario_creacion', 'usuario_modificacion']

    fieldsets = (
        (None, {
            'fields': ('producto', 'almacen', 'cantidad', 'stock_minimo', 'stock_maximo'),
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
    list_display = ['id', 'inventario', 'tipo', 'cantidad', 'get_usuario_creacion', 'fecha_creacion']
    search_fields = ['inventario', 'tipo']
    list_filter = ['tipo', 'inventario']
    
    readonly_fields = ['usuario_creacion','fecha_creacion']

    fieldsets = (
        (None, {
            'fields': ('inventario', 'tipo', 'cantidad'),
        }),
        ('Información Adicional', {
            'fields': ('usuario_creacion','fecha_creacion',),
            'classes': ('collapse',),
        }),
    )

    def get_usuario_creacion(self, obj):
        return obj.usuario_creacion.email if obj.usuario_creacion else "Sin usuario"
    get_usuario_creacion.short_description = "Usuario"

    # Sobrescribe save_model para asignar automáticamente el usuario autenticado
    def save_model(self, request, obj, form, change):
        if not change or not obj.usuario_creacion:
            obj.usuario_creacion = request.user
        super().save_model(request, obj, form, change)

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'inventario', 'tipo', 'leida']
    search_fields = ['inventario', 'tipo']
    list_filter = ['tipo', 'inventario']
    

    fieldsets = (
        (None, {
            'fields': ('inventario', 'tipo', 'leida'),
        }),
    )

