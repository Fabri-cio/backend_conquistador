from rest_framework import serializers
from ..productos.serializer import ProductoSerializer
from .models import Proveedor, OrdenCompra, DetalleOrden

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'

class OrdenCompraSerializer(serializers.ModelSerializer):
    # orden = serializers.PrimaryKeyRelatedField(queryset=OrdenCompra.objects.all())  # Solo el ID de la orden
    # proveedor = ProveedorSerializer()
    proveedor = serializers.PrimaryKeyRelatedField(queryset=Proveedor.objects.all())  # Solo retorna el ID del proveedor


    class Meta:
        model = OrdenCompra
        fields = '__all__'

class DetalleOrdenSerializer(serializers.ModelSerializer):
    # orden = OrdenCompraSerializer()
    orden = serializers.PrimaryKeyRelatedField(queryset=OrdenCompra.objects.all())  # Solo retorna el ID de la orden
    producto = ProductoSerializer()

    class Meta:
        model = DetalleOrden
        fields = '__all__'