from django.contrib import admin
from django import forms
from .models import Pedido, DetallePedido, Compra, DetalleCompra
from almacenes.models import Inventario


# --- Formulario personalizado para DetalleCompra ---
class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['id_inventario', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']

    def clean(self):
        cleaned_data = super().clean()
        id_inventario = cleaned_data.get('id_inventario')
        precio_unitario = cleaned_data.get('precio_unitario')

        # Si no se proporciona el precio unitario, autocompletarlo desde el producto relacionado
        if id_inventario and not precio_unitario:
            try:
                inventario = Inventario.objects.get(pk=id_inventario.pk)
                cleaned_data['precio_unitario'] = inventario.id_producto.precio  # Referencia desde producto
            except Inventario.DoesNotExist:
                raise forms.ValidationError("El inventario seleccionado no existe.")

        return cleaned_data


# --- Inline personalizado para DetalleCompra ---
class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    form = DetalleCompraForm  # Usa el formulario anterior
    extra = 1
    fields = ['id_inventario', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']
    readonly_fields = ['subtotal']

    def save_model(self, request, obj, form, change):
        # Calcular subtotal automáticamente: cantidad * precio - descuento
        obj.subtotal = (obj.cantidad * obj.precio_unitario) - obj.descuento_unitario
        super().save_model(request, obj, form, change)


# --- Admin para Compra ---
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id_compra', 'fecha_compra', 'id_usuario','id_tienda', 'pedido', 'total_compra']
    list_filter = ['fecha_compra', 'id_tienda']
    search_fields = ['id_compra', 'id_usuario__username', 'id_tienda__nombre']
    inlines = [DetalleCompraInline]
    readonly_fields = ['id_usuario', 'id_tienda', 'fecha_compra', 'total_compra']

    def save_model(self, request, obj, form, change):
        if not change:  # Asignar solo en la creación
            obj.id_usuario = request.user
            if request.user.lugar_de_trabajo:
                obj.id_tienda = request.user.lugar_de_trabajo
            else:
                raise forms.ValidationError("El usuario no tiene un almacén asignado en 'lugar_de_trabajo'.")
        super().save_model(request, obj, form, change)

        # Calcular el total de la venta
        total = sum(detalle.subtotal for detalle in obj.detalles.all())
        obj.total_compra = total
        obj.save()


# --- Inline para DetallePedido (si deseas mostrarlo dentro de Pedido) ---
class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1


# --- Admin para Pedido ---
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id_pedido', 'fecha_pedido', 'proveedor', 'usuario']
    list_filter = ['fecha_pedido', 'proveedor']
    search_fields = ['id_pedido', 'proveedor__nombre', 'usuario__username']
    inlines = [DetallePedidoInline]
    readonly_fields = ['fecha_pedido', 'usuario']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


# --- Registro en el admin ---
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(DetalleCompra)
admin.site.register(DetallePedido)
