from django.shortcuts import render
from django.contrib.auth.models import Permission

from seguridad.models import Usr
from seguridad.mkitsafe import *

@valida_acceso( [ 'permission.perms_permiso' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'permiso.permisos_permiso' ):
        toolbar.append( { 'type' : 'link', 'view' : 'permiso_inicio', 'label' : '<i class="fas fa-glasses"></i> Permisos' } )
    return render(
        request,
        'autenticacion/perms/index.html',
        {
            'data' : Permission.objects.all().order_by( 'content_type' ),
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Autenticacion/Permisos',
            'toolbar' : toolbar
        }
    )
