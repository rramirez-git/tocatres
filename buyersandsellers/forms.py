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
            'clave',
            'is_active', 
            'first_name', 
            'last_name', 
            'apellido_materno',
            'alias',
            'texto_productos',
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            'compra_a',
            'fiador',
            ]
        labels = {
            'email' : 'E-Mail',
            'last_name' : 'Apellido paterno'
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
            'clave',
            'is_active', 
            'first_name', 
            'last_name', 
            'apellido_materno',
            'alias',
            'texto_productos',
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            'compra_a',
            'fiador',
            ]
        labels = {
            'email' : 'E-Mail',
            'last_name' : 'Apellido paterno'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }

class RegClienteInVend( forms.ModelForm ):
    class Meta:
        model = Cliente
        fields = [ 
            'usuario', 
            'contraseña', 
            'clave',
            'is_active', 
            'first_name', 
            'last_name', 
            'apellido_materno',
            'alias',
            'texto_productos',
            'email', 
            'telefono', 
            'celular', 
            'fotografia',
            'fiador'
            ]
        labels = {
            'email' : 'E-Mail',
            'last_name' : 'Apellido paterno'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }

class RegClienteVend( forms.ModelForm ):
    class Meta:
        model = Cliente
        fields = [ 
            'usuario', 
            'clave',
            'is_active', 
            'first_name', 
            'last_name', 
            'apellido_materno',
            'alias',
            'texto_productos',
            'email', 
            'telefono', 
            'celular', 
            'fotografia',
            'fiador'
            ]
        labels = {
            'email' : 'E-Mail',
            'last_name' : 'Apellido paterno'
        }
        help_texts = {
            'is_active' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
        }

class RegDireccion( forms.ModelForm ):
    class Meta:
        model = Cliente
        fields = [
            'calle',
            'numero_interior',
            'numero_exterior',
            'codigo_postal',
            'colonia',
            'municipio',
            'estado'
        ]