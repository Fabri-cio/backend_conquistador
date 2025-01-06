from django.contrib import admin
from .models import Categoria, Proveedor, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre_categoria', 'descripcion']
    search_fields = ['nombre_categoria']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre_proveedor']
    search_fields = ['nombre_proveedor']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    # Cambiar el nombre de los campos y su formato
    list_display = ['nombre', 'precio', 'estado', 'get_user', 'get_fecha_creacion', 'get_fecha_modificacion']
    list_filter = ['estado', 'categoria']
    search_fields = ['nombre', 'codigo_barras']
    
    # Campos de solo lectura
    readonly_fields = ['id_user', 'fecha_creacion', 'fecha_modificacion']
    
    # Organizar los campos en el formulario
    fieldsets = (
        (None, {
            'fields': ('nombre', 'precio', 'codigo_barras', 'categoria', 'id_proveedor', 'estado'),
        }),
        ('Información Adicional', {
            'fields': ('id_user', 'fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',),  # Los hace colapsables
        }),
    )

    # Método para mostrar el id_user
    def get_user(self, obj):
        return obj.id_user.username  # Muestra el nombre de usuario del ID

    get_user.short_description = 'Creado Por'  # Título del campo en el admin

    # Métodos para formatear las fechas
    def get_fecha_creacion(self, obj):
        return obj.fecha_creacion.strftime('%d/%m/%Y %H:%M')  # Personaliza el formato de fecha

    get_fecha_creacion.short_description = 'Fecha de Creación'  # Título del campo en el admin

    def get_fecha_modificacion(self, obj):
        return obj.fecha_modificacion.strftime('%d/%m/%Y %H:%M')  # Personaliza el formato de fecha

    get_fecha_modificacion.short_description = 'Fecha de Modificación'  # Título del campo en el admin

    # Sobrescribe save_model para asignar automáticamente el usuario autenticado
    def save_model(self, request, obj, form, change):
        if not change or not obj.id_user:
            obj.id_user = request.user
        super().save_model(request, obj, form, change)
