from django import forms
from .models import *

class RegProductoCPrecio( forms.ModelForm ):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'sku',
            'imagen',
            'esta_activo',
            'marca',
            'modelo',
            'categoria',
            'precio_de_compra',
            'precio_de_venta',
            'descripcion'
        ]
        labels = {
            'sku' : 'SKU',
            'categoria' : 'Categoría',
            'descripcion' : 'Descripción',
            'precio_de_compra' : 'Costo',
            'precio_de_venta' : 'Precio'
        }

class RegProducto( forms.ModelForm ):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'sku',
            'imagen',
            'esta_activo',
            'marca',
            'modelo',
            'categoria',
            'descripcion'
        ]
        labels = {
            'sku' : 'SKU',
            'categoria' : 'Categoría',
            'descripcion' : 'Descripción'
        }

class RegCampaña( forms.ModelForm ):
    class Meta:
        model = Campaña
        fields = [
            'nombre',
            'fecha_de_inicio',
            'fecha_de_termino',
            'mostrar_precio_de_venta',
            'productos'
        ]
        widgets = {
            'fecha_de_inicio' : forms.TextInput( attrs = { 'type' : 'date' } ),
            'fecha_de_termino' : forms.TextInput( attrs = { 'type' : 'date' } )
        }
