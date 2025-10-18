from rest_framework import serializers
from predicciones.models import Prediccion, DetallePrediccion, ConfiguracionModelo
from django.db import transaction
from predicciones.services import PrediccionService
import datetime

class DetallePrediccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePrediccion
        fields = ['cantidad', 'fecha']

class PrediccionSerializer(serializers.ModelSerializer):
    detalles = DetallePrediccionSerializer(many=True)
    nombre_producto = serializers.CharField(source='inventario.producto.nombre', read_only=True)
    nombre_configuracion = serializers.CharField(source='configuracion.nombre', read_only=True)
    resultado = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Prediccion
        fields = [
            'id',
            'inventario',
            'configuracion',
            'nombre_producto',
            'nombre_configuracion',
            'fecha_inicio',
            'fecha_fin',
            'resultado',
            'detalles',
        ]

    def create(self, validated_data):
        detalles_data = validated_data.pop("detalles", [])
        with transaction.atomic():
            # Crear predicción con resultado temporal 0
            prediccion = Prediccion.objects.create(**validated_data, resultado=0)

            total_cantidad = 0
            for detalle in detalles_data:
                cantidad = round(detalle.get("cantidad", 0))
                total_cantidad += cantidad
                fecha = detalle.get("fecha")

                # Convertir string ISO a date si es necesario
                if isinstance(fecha, str):
                    if "T" in fecha:
                        fecha = fecha.split("T")[0]
                    fecha = datetime.date.fromisoformat(fecha)

                DetallePrediccion.objects.create(
                    prediccion=prediccion,
                    cantidad=cantidad,
                    fecha=fecha
                )

            # Guardar el total en resultado
            prediccion.resultado = total_cantidad
            prediccion.save()

        return prediccion


class ConfiguracionModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionModelo
        fields = '__all__'

class ConfigModelSelectIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfiguracionModelo
        fields = ['id', 'nombre']
