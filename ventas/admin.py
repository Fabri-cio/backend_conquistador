from django.contrib import admin
from .models import Venta, DetalleVenta
from productos.models import Producto
from django import forms


# Formulario personalizado para DetalleVenta
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['id_producto', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']

    def clean(self):
        cleaned_data = super().clean()
        id_producto = cleaned_data.get('id_producto')
        precio_unitario = cleaned_data.get('precio_unitario')

        # Si no se proporciona el precio unitario, autocompletarlo desde el producto
        if id_producto and not precio_unitario:
            try:
                producto = Producto.objects.get(pk=id_producto.pk)
                cleaned_data['precio_unitario'] = producto.precio
            except Producto.DoesNotExist:
                raise forms.ValidationError("El producto seleccionado no existe.")
        
        return cleaned_data


# Inline personalizado para DetalleVenta
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    form = DetalleVentaForm  # Usar el formulario personalizado
    extra = 1
    fields = ['id_producto', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']
    readonly_fields = ['subtotal']

    def save_model(self, request, obj, form, change):
        obj.subtotal = obj.cantidad * obj.precio_unitario - obj.descuento_unitario
        super().save_model(request, obj, form, change)


# Admin para Venta
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id_venta', 'fecha_venta', 'id_usuario', 'id_tienda', 'total_venta']
    list_filter = ['fecha_venta', 'id_tienda']
    search_fields = ['id_venta', 'id_usuario__username', 'id_tienda__nombre']
    inlines = [DetalleVentaInline]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        total = sum(detalle.subtotal for detalle in obj.detalles.all())
        obj.total_venta = total
        obj.save()


admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta)
