from django import forms
from django.contrib import auth

from .models import *

class RegPermiso( forms.ModelForm ):
    class Meta:
        model = Permiso
        fields = [ 'nombre', 'mostrar_como', 'permiso_padre', 'vista', 'posicion', 'es_operacion', 'content_type', 'descripcion' ]

class RegUsuario( forms.ModelForm ):
    class Meta:
        model = Usr
        fields = [ 
            'usuario', 
            'contraseña', 
            'is_active', 
            'is_superuser', 
            'first_name', 
            'last_name', 
            'email', 
            'telefono', 
            'celular', 
            'fotografia', 
            'groups', 
            'depende_de' 
        ]
        labels = {
            'email' : 'E-Mail',
            'groups' : 'Perfiles'
        }
        help_texts = {
            'groups' : '',
            'is_active' : '',
            'is_superuser' : ''
        }
        widgets = {
            'telefono' : forms.TextInput( attrs={ 'type' : 'tel' } ),
            'celular' : forms.TextInput( attrs={ 'type' : 'tel' } )
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
    def clean(self):
        username = self.cleaned_data.get( 'usr' )
        password = self.cleaned_data.get( 'pwd' )
        user = auth.authenticate( username = username, password = password)
        if not user or not user.is_active:
            raise forms.ValidationError( "El usuario o la contraseña no son válidos." )
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get( 'usr' )
        password = self.cleaned_data.get( 'pwd' )
        user = auth.authenticate( username = username, password = password )
        return user

class RegSetting( forms.ModelForm ):
    class Meta:
        model = Setting
        fields = [
            'seccion',
            'nombre',
            'nombre_para_mostrar',
            'tipo'
        ]