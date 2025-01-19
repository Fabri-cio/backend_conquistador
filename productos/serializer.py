from rest_framework import serializers
from .models import Categoria, Proveedor, Producto, User

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        # fields = ('id_categoria', 'nombre_categoria', 'descripcion')
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):

    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    nombre_categoria = serializers.CharField(source="categoria.nombre_categoria", read_only=True)
    nombre_proveedor = serializers.CharField(source="id_proveedor.nombre_proveedor", read_only=True)
    usuario_creacion = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    usuario_modificacion = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)


    class Meta:
        model = Producto
        fields = [
            "id_producto",        # ID del producto
            "estado",             # Estado del producto
            "nombre",             # Nombre del producto
            "precio",             # Precio del producto
            "codigo_barras",      # Código de barras
            "nombre_proveedor",   # Nombre del proveedor
            "nombre_categoria",   # Nombre de la categoría
            "usuario_creacion",
            "usuario_modificacion",
            "fecha_creacion",     # Fecha de creación
            "fecha_modificacion", # Fecha de modificación
        ]

    # Opcional: Ajustes en la representación (si deseas asegurar que el precio sea flotante)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Asegúrate de que el precio se represente como float en lugar de cadena
        representation['precio'] = float(representation['precio'])
        return representation
    
