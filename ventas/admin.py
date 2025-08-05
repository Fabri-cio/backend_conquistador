from django.contrib import admin
from .models import Venta, DetalleVenta, ComprobanteVenta, Cliente
from inventarios.models import Inventario
from django import forms


# Formulario personalizado para DetalleVenta
class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['id_inventario', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']

    def clean(self):
        cleaned_data = super().clean()
        id_inventario = cleaned_data.get('id_inventario')
        precio_unitario = cleaned_data.get('precio_unitario')

        # Si no se proporciona el precio unitario, autocompletarlo desde el producto relacionado
        if id_inventario and not precio_unitario:
            try:
                inventario = Inventario.objects.get(pk=id_inventario.pk)
                cleaned_data['precio_unitario'] = inventario.id_producto.precio  # Aquí el cambio
            except Inventario.DoesNotExist:
                raise forms.ValidationError("El inventario seleccionado no existe.")
        
        return cleaned_data



# Inline personalizado para DetalleVenta
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    form = DetalleVentaForm  # Usar el formulario personalizado
    extra = 1
    fields = ['id_inventario', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']
    readonly_fields = ['subtotal']

    def save_model(self, request, obj, form, change):
        obj.subtotal = (obj.cantidad * obj.precio_unitario) - obj.descuento_unitario
        super().save_model(request, obj, form, change)

# Admin para Venta
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id_venta', 'fecha_creacion', 'usuario_creacion', 'usuario_modificacion', 'id_tienda', 'total_venta']
    list_filter = ['fecha_creacion', 'id_tienda']
    search_fields = ['id_venta', 'usuario_creacion__username', 'id_tienda__nombre']
    inlines = [DetalleVentaInline]
    readonly_fields = ['usuario_creacion', 'usuario_modificacion', 'fecha_creacion', 'fecha_modificacion', 'id_tienda', 'total_venta']

    def save_model(self, request, obj, form, change):
        if not change:  # Asignar solo en la creación
            obj.usuario_creacion = request.user
            if request.user.lugar_de_trabajo:
                obj.id_tienda = request.user.lugar_de_trabajo
            else:
                raise forms.ValidationError("El usuario no tiene un almacén asignado en 'lugar_de_trabajo'.")
        super().save_model(request, obj, form, change)

        # Calcular el total de la venta
        total = sum(detalle.subtotal for detalle in obj.detalles.all())
        obj.total_venta = total
        obj.save()

admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta)
admin.site.register(ComprobanteVenta)
admin.site.register(Cliente)

