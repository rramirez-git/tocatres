from django import forms
from .models import *

class RegPermiso( forms.ModelForm ):
    class Meta:
        model = Permiso
        fields = [ 'nombre', 'permiso_padre', 'vista', 'posicion', 'es_operacion', 'content_type', 'descripcion' ]

class RegUsuario( forms.ModelForm ):
    class Meta:
        model = Usr
        fields = [ 'usuario', 'contraseña', 'is_active', 'is_superuser', 'first_name', 'last_name', 'email', 'telefono', 'celular', 'fotografia', 'groups', 'depende_de' ]
        labels = {
            'email' : 'E-Mail',
            'groups' : 'Perfiles'
        }
        help_texts = {
            'groups' : '',
            'is_active' : '',
            'is_superuser' : ''
        }

class AccUsuario( forms.Form ):
    usr = forms.CharField(
        label = "Usuario",
        max_length = 50,
        widget = forms.TextInput( attrs = { 
            'class' : 'form-control', 
            'autocomplete' : "off",
            'placeholder' : "Usuario",
            'autofocus' : "autofocus"
            } )
    )
    pwd = forms.CharField(
        label = "Contraseña",
        max_length = 250,
        widget = forms.PasswordInput( attrs = { 
            'class' : 'form-control', 
            'autocomplete' : "off",
            'placeholder' : "Contraseña" 
            } )
    )
