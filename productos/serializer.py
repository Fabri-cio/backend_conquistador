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

    categoria = serializers.CharField(source='categoria.nombre_categoria')

    # categoria = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all())  # Solo retorna el ID de la categoría

    class Meta:
        model = Producto    
        fields = '__all__'