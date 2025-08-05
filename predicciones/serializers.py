from rest_framework import serializers
from predicciones.models import Prediccion
from usuarios.models import Usuario
from inventarios.models import Inventario
from predicciones.models import DetallePrediccion, ConfiguracionModelo

class PrediccionSerializer(serializers.ModelSerializer):
    # Mostrar solo el ID para relaciones
    usuario_creacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.all(),
        source='usuario_creacion',
        write_only=True
    )
    inventario_id = serializers.PrimaryKeyRelatedField(
        queryset=Inventario.objects.all(),
        source='inventario',
        write_only=True
    )
    
    # Mostrar datos anidados para lectura
    usuario_creacion = serializers.StringRelatedField(read_only=True)
    inventario = serializers.StringRelatedField(read_only=True)

    resultado_prediccion = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        model = Prediccion
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convertir resultado_prediccion a float para JSON más amigable
        representation['resultado_prediccion'] = float(representation['resultado_prediccion'])
        return representation


class DetallePrediccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePrediccion
        fields = '__all__'


class ConfiguracionModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionModelo
        fields = '__all__'
