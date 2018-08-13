from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import auth

from .forms import *
from .models import *
from .mkitsafe import *

# Create your views here.
@valida_acceso()
def index( request ):
    return render( 
        request, 
        'global/html_struct.html', 
        {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Bienvenido',
            'titulo_descripcion' : request.user.get_full_name()
        } )

def login( request ):
    frm = AccUsuario( request.POST or None )
    if frm.is_valid() and 'POST' == request.method:
        user = frm.login( request )
        if user is not None and user.is_active:
            auth.login( request, user )
            usuario = Usr.objects.get( id = user.pk )
            request.session[ 'usuario' ] = usuario.pk
            request.session[ 'usuario_pic' ] = "{}".format( usuario.fotografia )
            return HttpResponseRedirect( reverse( 'seguridad_inicio' ) )
    auth.logout( request )
    return render( 
        request, 
        'seguridad_login.html', {
        'footer' : True,
        'frm' : frm
    } )

def logout( request ):
    return HttpResponseRedirect( reverse( 'seguridad_login' ) )