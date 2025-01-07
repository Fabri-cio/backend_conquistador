from django import forms
from productos.models import Producto
from .models import DetalleVenta

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['id_producto', 'cantidad', 'precio_unitario', 'descuento_unitario', 'subtotal']

    # Campo de búsqueda personalizado por código de barras
    id_producto = forms.ModelChoiceField(
        queryset=Producto.objects.filter(estado=True),  # Filtra solo los productos activos (en estado True)
        empty_label="Buscar por código de barras",
        to_field_name="codigo_barras",  # Utiliza 'codigo_barras' para la búsqueda
        required=True,
        widget=forms.Select(attrs={'class': 'vSelect2'})
    )
