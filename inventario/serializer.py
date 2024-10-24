from rest_framework import serializers
from .models import Inventario

class InventarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventario
        # fields = ('id_inventario', 'producto', 'cantidad_disponible', 'ubicacion_almacen')  # Campos explícitos
        fields = '__all__'