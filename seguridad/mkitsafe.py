""" Módulo para verificación de permisos de usuarios """

from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Permiso
from tocatres.utils import *

def valida_acceso( permisos = None ):
    url_error = 'seguridad_inicio'
    url_autenticacion = 'seguridad_login'
    """ 
    Función decoradora que verifica si un usuario esta logeado en el sistema y si tiene ALGUNO de los permisos pasados como parámetro o bien alguno de los permisos hijo 
    
    Parámetros:

        permisos = None 
            Lista de permisos a validar, en caso de recibir None sólo se valida que el usuario este logeado en el sistema
            Cada permiso debe estar en formato de cadena 'modelo.codename'
        url_error = 'seguridad_inicio'
            Nombre de la URL a la que se redireccionará en caso de que el usuario no cuente con ningún permiso
        url_autenticacion = 'seguridad_login'
            Nombre de la URL a la que se redireccionará en caso de que el usuario no esté logeado en el sistema
    """

    def _valida_acceso( vista ):
        """ Función de segundo nivel de la función decoradora valida_acceso """

        def validacion( *args, **kwargs ):
            """ Funcion de tercer nivel de la función decoradora valida_acceso """
            usuario = args[ 0 ].user
            if not usuario.is_authenticated:
                print_error( "Vista {} negada por autenticación".format( vista.__name__ ), "Exec Info" )
                return HttpResponseRedirect( reverse( url_autenticacion ) )
            if permisos is None:
                return vista( *args, **kwargs )
            perms = []
            for perm in permisos:
                permiso = Permiso.get_from_package_codename( perm )
                if( permiso is None ):
                    print_error( "No se ha encontrado el permiso: " + perm )
                else:
                    perms.append( permiso.perm() )
                    desc = permiso.descendencia()
                    for p in desc:
                        perms.append( p.perm() )
            for perm in perms:
                p = "{}.{}".format( perm.content_type.app_label, perm.codename )
                if usuario.has_perm( p ):
                    return vista( *args, **kwargs )
            print_error( "Vista {} negada por permisos {}".format( vista.__name__, permisos ), "Exec Info" )
            return HttpResponseRedirect( reverse( url_error ) )
        return validacion

    return _valida_acceso

            