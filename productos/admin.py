from django.contrib import admin
from .models import Categoria, Proveedor, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['marca', 'nombre_contacto', 'telefono', 'estado', 'imagen']
    search_fields = ['marca']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = [
        'nombre', 'precio', 'estado', 'imagen', 'get_usuario_creacion', 'get_usuario_modificacion',
        'get_fecha_creacion', 'get_fecha_modificacion'
    ]
    list_filter = ['estado', 'categoria']
    search_fields = ['nombre', 'codigo_barras']
    readonly_fields = ['usuario_creacion', 'usuario_modificacion', 'fecha_creacion', 'fecha_modificacion']

    fieldsets = (
        (None, {
            'fields': ('nombre', 'precio', 'codigo_barras', 'categoria', 'proveedor', 'estado', 'imagen', 'documento'),
        }),
        ('Información Adicional', {
            'fields': ('usuario_creacion', 'usuario_modificacion', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',),
        }),
    )

    def get_usuario_creacion(self, obj):
        return obj.usuario_creacion.email if obj.usuario_creacion else "No asignado"

    get_usuario_creacion.short_description = "Creado por"

    def get_usuario_modificacion(self, obj):
        return obj.usuario_modificacion.email if obj.usuario_modificacion else "no modificado"

    get_usuario_modificacion.short_description = "Modificado por"

    def get_fecha_creacion(self, obj):
        return obj.fecha_creacion.strftime('%d/%m/%Y %H:%M')

    get_fecha_creacion.short_description = "Fecha de creación"

    def get_fecha_modificacion(self, obj):
        return obj.fecha_modificacion.strftime('%d/%m/%Y %H:%M')

    get_fecha_modificacion.short_description = "Fecha de modificación"

    def save_model(self, request, obj, form, change):
        if not change or not obj.usuario_creacion:
            obj.usuario_creacion = request.user
        obj.usuario_modificacion = request.user
        super().save_model(request, obj, form, change)
