from django import forms
from .models import *

class RegVendedorIn( forms.ModelForm ):
    class Meta:
        model = Vendedor
        fields = [ 'usuario', 'contraseña', 'is_active', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'fotografia', 'reporta_a' ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }

class RegVendedor( forms.ModelForm ):
    class Meta:
        model = Vendedor
        fields = [ 'usuario', 'is_active', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'fotografia', 'reporta_a' ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }
class RegClienteIn( forms.ModelForm ):
    class Meta:
        model = Cliente
        fields = [ 'usuario', 'contraseña', 'is_active', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'fotografia', 'compra_a' ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }

class RegCliente( forms.ModelForm ):
    class Meta:
        model = Cliente
        fields = [ 'usuario', 'is_active', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'fotografia', 'compra_a' ]
        labels = {
            'email' : 'E-Mail'
        }
        help_texts = {
            'is_active' : ''
        }
