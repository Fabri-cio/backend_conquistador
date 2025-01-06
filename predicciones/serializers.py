from rest_framework import serializers
from .models import Prediccion
from usuarios.models import CustomUser
from productos.models import Producto

class PrediccionSerializer(serializers.ModelSerializer):
    # Mostrar solo el ID para relaciones
    usuario_responsable_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='usuario_responsable',
        write_only=True
    )
    producto_id = serializers.PrimaryKeyRelatedField(
        queryset=Producto.objects.all(),
        source='producto',
        write_only=True
    )
    
    # Mostrar datos anidados para lectura
    usuario_responsable = serializers.StringRelatedField(read_only=True)
    producto = serializers.StringRelatedField(read_only=True)

    resultado_prediccion = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        model = Prediccion
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convertir resultado_prediccion a float para JSON más amigable
        representation['resultado_prediccion'] = float(representation['resultado_prediccion'])
        return representation
