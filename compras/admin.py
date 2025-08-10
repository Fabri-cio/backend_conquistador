from django.contrib import admin
from django import forms
from .models import Pedido, DetallePedido, Compra, DetalleCompra
from inventarios.models import Inventario


# --- Formulario personalizado para DetalleCompra ---
class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['inventario', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']

    def clean(self):
        cleaned_data = super().clean()
        inventario = cleaned_data.get('inventario')
        precio_unitario = cleaned_data.get('precio_unitario')

        # Si no se proporciona el precio unitario, autocompletarlo desde el producto relacionado
        if inventario and not precio_unitario:
            try:
                inventario = Inventario.objects.get(pk=inventario.pk)
                cleaned_data['precio_unitario'] = inventario.producto.precio  # Referencia desde producto
            except Inventario.DoesNotExist:
                raise forms.ValidationError("El inventario seleccionado no existe.")

        return cleaned_data


# --- Inline personalizado para DetalleCompra ---
class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    form = DetalleCompraForm  # Usa el formulario anterior
    extra = 1
    fields = ['inventario', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']
    readonly_fields = ['subtotal']

    def save_model(self, request, obj, form, change):
        # Calcular subtotal automáticamente: cantidad * precio - descuento
        obj.subtotal = (obj.cantidad * obj.precio_unitario) - obj.descuento_unitario
        super().save_model(request, obj, form, change)


# --- Admin para Compra ---
class CompraAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_creacion', 'usuario_creacion','pedido', 'total_compra']
    list_filter = ['fecha_creacion']
    search_fields = ['id', 'usuario_creacion__username']
    inlines = [DetalleCompraInline]
    readonly_fields = ['usuario_creacion', 'fecha_creacion', 'fecha_modificacion', 'usuario_modificacion', 'total_compra']

    def save_model(self, request, obj, form, change):
        if not change:  # Asignar solo en la creación
            obj.usuario_creacion = request.user
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
    list_display = ['id', 'fecha_creacion', 'proveedor', 'usuario_creacion', 'usuario_modificacion', 'fecha_modificacion']
    list_filter = ['fecha_creacion', 'proveedor']
    search_fields = ['id', 'proveedor__nombre', 'usuario_creacion__username']
    inlines = [DetallePedidoInline]
    readonly_fields = ['fecha_creacion', 'usuario_creacion', 'usuario_modificacion', 'fecha_modificacion']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_creacion = request.user
        super().save_model(request, obj, form, change)


# --- Registro en el admin ---
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Compra, CompraAdmin)
admin.site.register(DetalleCompra)
admin.site.register(DetallePedido)
