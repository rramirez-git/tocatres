from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, Permission
from django.db.models import ProtectedError

from .models import *
from .vw_permiso import PermisoTableStruct
from .mkitsafe import *

@valida_acceso( [ 'group.perfiles_grupo' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'group.agregar_perfiles_grupo' ):
        toolbar.append( { 'type' : 'link', 'view' : 'perfil_nuevo', 'label' : '<i class="far fa-file"></i> Nuevo' } )
    return render( 
        request, 
        'seguridad/perfil/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Perfiles',
            'data' : Group.objects.all().order_by( 'name' ),
            'toolbar' : toolbar
        } )

@valida_acceso( [ 'group.agregar_perfiles_grupo' ] )
def new( request ):
    if 'POST' == request.method:
        obj = Group.objects.create( name = request.POST.get( 'nombre' ) )
        obj.save()
        for p in request.POST.getlist( 'permisos' ):
            perm = Permiso.objects.get( pk = p )
            obj.permissions.add( perm )
        obj.save()
        return HttpResponseRedirect( reverse( 'perfil_ver', kwargs = { 'pk' : obj.pk } ) )
    root_perms = Permiso.objects.filter( permiso_padre__isnull = True ).order_by( 'posicion' )
    permisos = []
    for obj in root_perms:
        aux = PermisoTableStruct( obj )
        for p in aux:
            permisos.append( p )
    return render( 
        request, 
        'seguridad/perfil/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Perfiles',
            'titulo_descripcion' : 'Nuevo',
            'permisos' : permisos
        } )

@valida_acceso( [ 'group.perfiles_grupo' ] )
def see( request, pk ):
    if not Group.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    gpo = Group.objects.get( pk = pk )
    root_perms = Permiso.objects.filter( permiso_padre__isnull = True ).order_by( 'posicion' )
    permisos = []
    permisos_en_perfil = []
    for obj in root_perms:
        aux = PermisoTableStruct( obj )
        for p in aux:
            permisos.append( p )
            if Permission.objects.get( pk = p.id ) in gpo.permissions.all():
                permisos_en_perfil.append( p )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'group.perfiles_grupo' ):
        toolbar.append( { 'type' : 'link', 'view' : 'perfil_inicio', 'label' : '<i class="fas fa-list-ul"></i> Ver todos' } )
    if usuario.has_perm_or_has_perm_child( 'group.actualizar_perfiles_grupo' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'perfil_actualizar', 'label' : '<i class="far fa-edit"></i> Actualizar', 'pk' : pk } )
    if usuario.has_perm_or_has_perm_child( 'group.eliminar_perfiles_grupo' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'perfil_eliminar', 'label' : '<i class="far fa-trash-alt"></i> Eliminar', 'pk' : pk } )
    return render(
        request,
        'seguridad/perfil/form.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Perfiles',
            'titulo_descripcion' : gpo.name,
            'gpo' : gpo,
            'permisos' : permisos,
            'permisos_en_perfil' : permisos_en_perfil,
            'read_only' : True,
            'toolbar' : toolbar
        }
    )

@valida_acceso( [ 'group.actualizar_perfiles_grupo' ] )
def update( request, pk ):
    if not Group.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    gpo = Group.objects.get( pk = pk )
    if "POST" == request.method:
        gpo.name = request.POST.get( 'nombre' )
        gpo.save()
        gpo.permissions.clear()
        for p in request.POST.getlist( 'permisos' ):
            perm = Permiso.objects.get( pk = p )
            gpo.permissions.add( perm )
            gpo.save()
        return HttpResponseRedirect( reverse( 'perfil_ver', kwargs = { 'pk' : gpo.pk } ) )
    root_perms = Permiso.objects.filter( permiso_padre__isnull = True ).order_by( 'posicion' )
    permisos = []
    permisos_en_perfil = []
    for obj in root_perms:
        aux = PermisoTableStruct( obj )
        for p in aux:
            permisos.append( p )
            if Permission.objects.get( pk = p.id ) in gpo.permissions.all():
                permisos_en_perfil.append( p )
    return render(
        request,
        'seguridad/perfil/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Perfiles',
            'titulo_descripcion' : gpo.name,
            'gpo' : gpo,
            'permisos' : permisos,
            'permisos_en_perfil' : permisos_en_perfil
        }
    )

@valida_acceso( [ 'group.eliminar_perfiles_grupo' ] )
def delete( request, pk ):
    try:
        if not Group.objects.filter( pk = pk ).exists():
            return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
        Group.objects.get( pk = pk ).delete()
        return HttpResponseRedirect( reverse( 'perfil_inicio' ) )
    except ProtectedError:
        return HttpResponseRedirect( reverse( 'seguridad_item_con_relaciones' ) )
