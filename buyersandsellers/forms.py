from django import forms
from .models import *

class RegVendedorInAdmin( forms.ModelForm ):
    class Meta:
        model = Vendedor
        fields = [ 
            'usuario', 
            'contraseña', 
            'is_active', 
            'first_name', 
            'last_name', 
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            'reporta_a' 
            ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }

class RegVendedorAdmin( forms.ModelForm ):
    class Meta:
        model = Vendedor
        fields = [ 
            'usuario', 
            'is_active', 
            'first_name', 
            'last_name', 
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            'reporta_a' 
            ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }

class RegVendedorIn( forms.ModelForm ):
    class Meta:
        model = Vendedor
        fields = [ 
            'usuario', 
            'contraseña', 
            'is_active', 
            'first_name', 
            'last_name', 
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }

class RegVendedor( forms.ModelForm ):
    class Meta:
        model = Vendedor
        fields = [ 
            'usuario', 
            'is_active', 
            'first_name', 
            'last_name', 
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }

class RegClienteIn( forms.ModelForm ):
    class Meta:
        model = Cliente
        fields = [ 
            'usuario', 
            'contraseña', 
            'is_active', 
            'first_name', 
            'last_name', 
            'alias',
            'texto_productos',
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            'compra_a' 
            ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }

class RegCliente( forms.ModelForm ):
    class Meta:
        model = Cliente
        fields = [ 
            'usuario', 
            'is_active', 
            'first_name', 
            'last_name', 
            'alias',
            'texto_productos',
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            'compra_a' 
            ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }
