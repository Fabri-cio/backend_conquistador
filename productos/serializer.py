from rest_framework import serializers
from .models import Categoria, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        # fields = ('id_categoria', 'nombre_categoria', 'descripcion')
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # Serializador anidado para mostrar los detalles de la categoría
    # categoria = CategoriaSerializer()

    #categoria = serializers.CharField(source='categoria.nombre_categoria')

    precio = serializers.DecimalField(max_digits=10, decimal_places=2)

    categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())  # Solo retorna el ID de la categoría

    class Meta:
        model = Producto    
        fields = '__all__'

    # Opcional: Ajustes en la representación (si deseas asegurar que el precio sea flotante)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Asegúrate de que el precio se represente como float en lugar de cadena
        representation['precio'] = float(representation['precio'])
        return representation