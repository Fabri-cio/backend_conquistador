from rest_framework import serializers
from .models import Categoria, Proveedor, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        # fields = ('id_categoria', 'nombre_categoria', 'descripcion')
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class ProductoListSerializer(serializers.ModelSerializer):
    nombre_categoria = serializers.CharField(source="categoria.nombre_categoria", read_only=True)
    nombre_proveedor = serializers.CharField(source="id_proveedor.nombre_proveedor", read_only=True)
    class Meta:
        model = Producto
        fields = [
            "id_producto",        
            "estado",             
            "nombre",             
            "precio",                     
            "nombre_proveedor",   
            "nombre_categoria",
            "imagen",  
            "documento",
        ]
    
class ProductoDetailSerializer(serializers.ModelSerializer):
    precio = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Producto
        fields = [
            "id_producto",        
            "estado",             
            "nombre",             
            "precio",             
            "codigo_barras",      
            "id_proveedor",
            "categoria",
            "imagen",
            "documento",
        ]

class ProductoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = [        
            "estado",             
            "nombre",             
            "precio",             
            "codigo_barras",      
            "id_proveedor",
            "categoria",
            "usuario_creacion",
            "usuario_modificacion",
            "imagen",
            "documento",
        ]
