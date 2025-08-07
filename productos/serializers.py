from rest_framework import serializers
from .models import Categoria, Proveedor, Producto
from django.utils.translation import gettext_lazy as _

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
    nombre_categoria = serializers.CharField(source="categoria.nombre", read_only=True)
    nombre_proveedor = serializers.CharField(source="proveedor.nombre", read_only=True)
    class Meta:
        model = Producto
        fields = [
            "id",        
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
            "id",        
            "estado",             
            "nombre",             
            "precio",             
            "codigo_barras",      
            "proveedor",
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
            "proveedor",
            "categoria",
            "imagen",
            "documento",
        ]

    def validate_codigo_barras(self, value):
        if Producto.objects.filter(codigo_barras=value).exists():
            raise serializers.ValidationError(
                _("Ya existe un producto con este código de barras.")
            )
        return value

class ProductoHistorySerializer(serializers.ModelSerializer):
    history_type = serializers.CharField()
    history_date = serializers.DateTimeField()
    history_user = serializers.SerializerMethodField()
    cambios = serializers.SerializerMethodField()

    class Meta:
        model = Producto.history.model
        fields = [
            'id',
            'nombre',
            'precio',
            'history_type',
            'history_date',
            'history_user',
            'cambios',  # <- campo extra para mostrar qué cambió
        ]

    def get_history_user(self, obj):
        return str(obj.history_user) if obj.history_user else None

    def get_cambios(self, obj):
        previous = obj.prev_record
        if not previous:
            return None
        delta = obj.diff_against(previous)
        cambios = {}
        for change in delta.changes:
            cambios[change.field] = {
                "de": change.old,
                "a": change.new,
            }
        return cambios


