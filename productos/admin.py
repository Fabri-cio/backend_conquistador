from django.contrib import admin
from .models import Categoria, Proveedor, Producto
from django.utils.timezone import now

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
        'nombre', 'precio', 'estado', 'imagen'
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

    # tener cuidado ya que esto solo funciona en el admin la api no funciona aqui
    def save_model(self, request, obj, form, change):
        if not change or not obj.usuario_creacion:
            obj.usuario_creacion = request.user
        else:
            obj.usuario_modificacion = request.user
            obj.fecha_modificacion = now()
        super().save_model(request, obj, form, change)
