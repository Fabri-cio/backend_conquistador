# Generated by Django 5.1.4 on 2025-01-06 22:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productos', '0002_alter_producto_id_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Almacen',
            fields=[
                ('id_almacen_tienda', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMovimiento',
            fields=[
                ('id_tipo', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_inventario', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.PositiveIntegerField(default=0)),
                ('stock_minimo', models.PositiveIntegerField(default=0)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('comentario_modificacion', models.TextField(blank=True, null=True)),
                ('id_almacen_tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacenes.almacen')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
                ('usuario_creacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventario_creado', to=settings.AUTH_USER_MODEL)),
                ('usuario_modificacion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventario_modificado', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id_movimiento', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad', models.IntegerField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('id_destino', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movimientos_entrada', to='almacenes.almacen')),
                ('id_origen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movimientos_salida', to='almacenes.almacen')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.producto')),
                ('id_usuario', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='almacenes.tipomovimiento')),
            ],
            options={
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
