from django.shortcuts import render
from django.contrib.auth.models import User

from seguridad.models import Usr
from seguridad.mkitsafe import *

@valida_acceso( [ 'user.users_usuario' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'usr.usuarios_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'usuario_inicio', 'label' : '<i class="fas fa-glasses"></i> Usuarios' } )
    return render(
        request,
        'autenticacion/users/index.html',
        {
            'data' : User.objects.all(),
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Autenticacion/Usuarios',
            'toolbar' : toolbar
        }
    )