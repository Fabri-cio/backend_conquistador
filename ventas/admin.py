# admin.py
from django.contrib import admin
from .models import Venta, DetalleVenta, ComprobanteVenta, Cliente
from django import forms

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['inventario', 'cantidad', 'precio_unitario', 'descuento_unitario', 'sub_total']

    def clean(self):
        data = super().clean()
        inventario = data.get('inventario')
        if inventario and not data.get('precio_unitario'):
            data['precio_unitario'] = inventario.producto.precio
        return data

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    form = DetalleVentaForm
    extra = 1
    readonly_fields = ['sub_total']

class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'fecha_creacion', 'usuario_creacion', 'tienda', 'total_venta']
    inlines = [DetalleVentaInline]
    readonly_fields = ['usuario_creacion', 'fecha_creacion', 'total_venta', 'tienda']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario_creacion = request.user
            obj.tienda = request.user.lugar_de_trabajo
        super().save_model(request, obj, form, change)

admin.site.register(Venta, VentaAdmin)
admin.site.register(DetalleVenta)
admin.site.register(ComprobanteVenta)
admin.site.register(Cliente)
