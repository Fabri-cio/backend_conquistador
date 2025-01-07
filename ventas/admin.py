from django.contrib import admin
from .models import Venta, DetalleVenta
from django import forms

# Formulario para la venta que permite elegir múltiples productos
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1  # Número de formularios vacíos a mostrar
    fields = ['id_producto', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']  # Campos que quieres mostrar en el admin
    readonly_fields = ['subtotal']  # Hacer solo lectura el campo subtotal

    # Si deseas calcular el subtotal automáticamente
    def save_model(self, request, obj, form, change):
        obj.subtotal = obj.cantidad * obj.precio_unitario - obj.descuento_unitario
        super().save_model(request, obj, form, change)

class VentaAdmin(admin.ModelAdmin):
    list_display = ['id_venta', 'fecha_venta', 'id_usuario', 'id_tienda', 'total_venta']
    list_filter = ['fecha_venta', 'id_tienda']
    search_fields = ['id_venta', 'id_usuario__username', 'id_tienda__nombre']
    
    # Incluir los detalles de la venta en la vista de la venta
    inlines = [DetalleVentaInline]

    # Personalizar la forma en que se guarda la venta
    def save_model(self, request, obj, form, change):
        # Llamar a la función de guardado por defecto
        super().save_model(request, obj, form, change)

        # Calcular el total de la venta, sumando los subtotales de los detalles
        total = sum(detalle.subtotal for detalle in obj.detalles.all())
        obj.total_venta = total
        obj.save()

admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta)
