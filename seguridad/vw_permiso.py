from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
from django.db.models import ProtectedError

from .forms import *
from .models import *
from .mkitsafe import *

@valida_acceso( [ 'permiso.permisos_permiso' ] )
def index( request ):
    root_perms = Permiso.objects.filter( permiso_padre__isnull = True ).order_by( 'posicion' )
    data = []
    for obj in root_perms:
        aux = PermisoTableStruct( obj )
        for p in aux:
            data.append( p )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'permiso.agregar_permisos_permiso' ):
        toolbar.append( { 'type' : 'link', 'view' : 'permiso_nuevo', 'label' : '<i class="far fa-file"></i> Nuevo' } )
    if usuario.has_perm_or_has_perm_child( 'permission.perms_permiso' ):
        toolbar.append( { 'type' : 'link', 'view' : 'perms_inicio', 'label' : '<i class="fas fa-glasses"></i> Perms' } )
    return render( 
        request, 
        'seguridad/permiso/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Permisos',
            'data' : data,
            'toolbar' : toolbar
        } )

@valida_acceso( [ 'permiso.agregar_permisos_permiso' ] )
def new( request ):
    frm = RegPermiso( request.POST or None )
    if frm.is_valid():
        obj = frm.save( commit = False )
        obj.name = obj.nombre
        obj.codename = "{}_{}".format( clean_name( obj.nombre ), obj.content_type )
        obj.save()
        return HttpResponseRedirect( reverse( 'permiso_ver', kwargs = { 'pk' : obj.pk } ) )
    return render( 
        request, 
        'global/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Permisos',
            'titulo_descripcion' : 'Nuevo',
            'frm' : frm
        } )

@valida_acceso( [ 'permiso.permisos_permiso' ] )
def see( request, pk ):
    if not Permiso.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    obj = Permiso.objects.get( pk = pk )
    frm = RegPermiso( instance = obj )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'permiso.permisos_permiso' ):
        toolbar.append( { 'type' : 'link', 'view' : 'permiso_inicio', 'label' : '<i class="fas fa-list-ul"></i> Ver todos' } )
    if usuario.has_perm_or_has_perm_child( 'permiso.actualizar_permisos_permiso' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'permiso_actualizar', 'label' : '<i class="far fa-edit"></i> Actualizar', 'pk' : pk } )
    if usuario.has_perm_or_has_perm_child( 'permiso.eliminar_permisos_permiso' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'permiso_eliminar', 'label' : '<i class="far fa-trash-alt"></i> Eliminar', 'pk' : pk } )
    return render(
        request,
        #'global/form.html', {
        'seguridad/permiso/see.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Permisos',
            'titulo_descripcion' : obj,
            'read_only' : True,
            'frm' : frm,
            'toolbar' : toolbar,
            'arbol' : PermisoStruct( obj )
        }
    )

@valida_acceso( [ 'permiso.actualizar_permisos_permiso' ] )
def update( request, pk ):
    if not Permiso.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    obj = Permiso.objects.get( pk = pk )
    if "POST" == request.method:
        frm = RegPermiso( instance = obj, data = request.POST )
        if frm.is_valid():
            obj = frm.save( commit = False)
            obj.name = obj.nombre
            obj.codename = "{}_{}".format( clean_name( obj.nombre ), obj.content_type )
            obj.save()
            return HttpResponseRedirect( reverse( 'permiso_ver', kwargs = { 'pk' : obj.pk } ) )
        else:
            return render(
                request,
                'global/form.html', {
                    'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
                    'footer' : True,
                    'titulo' : 'Permisos',
                    'titulo_descripcion' : obj,
                    'frm' : frm
                }
            )
    else:
        frm = RegPermiso( instance = obj )
        return render(
            request,
            'global/form.html', {
                'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
                'footer' : True,
                'titulo' : 'Permisos',
                'titulo_descripcion' : obj,
                'frm' : frm
            }
        )

@valida_acceso( [ 'permiso.eliminar_permisos_permiso' ] )
def delete( request, pk ):
    try:
        if not Permiso.objects.filter( pk = pk ).exists():
            return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
        obj = Permiso.objects.get( pk = pk )
        obj.delete()
        return HttpResponseRedirect( reverse( 'permiso_inicio' ) )
    except ProtectedError:
        return HttpResponseRedirect( reverse( 'seguridad_item_con_relaciones' ) )

def PermisoStruct( permiso, level = 0 ):
    linea = '{}{}<br />'.format( "&nbsp;" * ( level * 4 ), permiso )
    for p in permiso.hijos():
        linea += PermisoStruct( p, level + 1 )
    return linea

def PermisoTableStruct( permiso ):
    hijos = [ permiso ]
    aux = Permiso.objects.filter( permiso_padre__pk = permiso.pk ).order_by( 'posicion' )
    for p in aux:
        aux2 = PermisoTableStruct( p )
        for p2 in aux2:
            hijos.append( p2 )
    return hijos

def clean_name( name, to_lower = True ):
    name = name.replace( " ","_" )
    name = name.replace( "ñ", "n" )
    name = name.replace( "Ñ", "N" )
    name = name.replace( "á", "a" )
    name = name.replace( "Á", "A" )
    name = name.replace( "é", "e" )
    name = name.replace( "É", "E" )
    name = name.replace( "í", "i" )
    name = name.replace( "Í", "I" )
    name = name.replace( "ó", "o" )
    name = name.replace( "Ó", "O" )
    name = name.replace( "ú", "u" )
    name = name.replace( "U", "U" )
    name = name.replace( "ä", "a" )
    name = name.replace( "Ä", "A" )
    name = name.replace( "ë", "e" )
    name = name.replace( "ë", "E" )
    name = name.replace( "ï", "i" )
    name = name.replace( "Ï", "I" )
    name = name.replace( "ö", "o" )
    name = name.replace( "ö", "O" )
    name = name.replace( "ü", "u" )
    name = name.replace( "Ü", "U" )
    if True == to_lower:
        name = name.lower()
    return name
