from rest_framework import serializers
from .models import Inventario
from productos.models import Producto

class InventarioSerializer(serializers.ModelSerializer):
    producto = serializers.PrimaryKeyRelatedField(queryset=Producto.objects.all())  # Solo el ID del cliente

    class Meta:
        model = Inventario
        # fields = ('id_inventario', 'producto', 'cantidad_disponible', 'ubicacion_almacen')  # Campos explícitos
        fields = '__all__'