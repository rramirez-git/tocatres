from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from .forms import *
from .models import *
from .mkitsafe import *

@valida_acceso( [ 'usr.usuarios_usuario' ] )
def index( request ):
    root_usrs = Usr.objects.filter( depende_de__isnull = True )
    data = []
    for obj in root_usrs:
        data.append( obj )
        for h in obj.descendencia():
            data.append( h )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'usr.agregar_usuarios_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'usuario_nuevo', 'label' : '<i class="far fa-file"></i> Nuevo' } )
    if usuario.has_perm_or_has_perm_child( 'user.users_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'users_inicio', 'label' : '<i class="fas fa-glasses"></i> Users' } )
    return render(
        request,
        'seguridad/usuario/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Usuarios',
            'data' : data,
            'toolbar' : toolbar
        } )

@valida_acceso( [ 'usr.agregar_usuarios_usuario' ] )
def new( request ):
    if 'POST' == request.method:
        frm = RegUsuario( request.POST, files = request.FILES  )
        if frm.is_valid():
            obj = frm.save( commit = False )
            obj.username = obj.usuario
            obj.set_password( obj.contraseña )
            obj.save()
            for g in request.POST.getlist( 'groups' ):
                obj.groups.add( g )
            obj.save()
            return HttpResponseRedirect( reverse( 'usuario_ver', kwargs = { 'pk' : obj.pk } ) )
    frm = RegUsuario( request.POST or None )
    return render( request, 'global/form.html', {
        'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Usuarios',
            'titulo_descripcion' : 'Nuevo',
            'frm' : frm
    } )

@valida_acceso( [ 'usr.usuarios_usuario' ] )
def see( request, pk ):
    obj = Usr.objects.get( pk = pk )
    frm = RegUsuario( instance = obj )
    arbol = [ obj ]
    for u in obj.descendencia():
        arbol.append( u )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'usr.usuarios_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'usuario_inicio', 'label' : '<i class="fas fa-list-ul"></i> Ver todos' } )
    if usuario.has_perm_or_has_perm_child( 'usr.actualizar_usuarios_usuario' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'usuario_actualizar', 'label' : '<i class="far fa-edit"></i> Actualizar', 'pk' : pk } )
    if usuario.has_perm_or_has_perm_child( 'usr.eliminar_usuarios_usuario' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'usuario_eliminar', 'label' : '<i class="far fa-trash-alt"></i> Eliminar', 'pk' : pk } )
    return render( request, 'seguridad/usuario/see.html', {
        'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Usuarios',
            'titulo_descripcion' : obj,
            'read_only' : True,
            'frm' : frm,
            'fotografia' : obj.fotografia,
            'toolbar' : toolbar,
            'arbol' : arbol
    } )

@valida_acceso( [ 'usr.actualizar_usuarios_usuario' ] )
def update( request, pk ):
    usr = Usr.objects.get( pk = pk )
    if 'POST' == request.method:
        frm = RegUsuario( instance = usr, data = request.POST, files = request.FILES  )
        if frm.is_valid():
            obj = frm.save( commit = False )
            obj.username = obj.usuario
            obj.set_password( obj.contraseña )
            obj.save()
            obj.groups.clear()
            for g in request.POST.getlist( 'groups' ):
                obj.groups.add( g )
            obj.save()
            return HttpResponseRedirect( reverse( 'usuario_ver', kwargs = { 'pk' : obj.pk } ) )
        else:
            return render( request, 'global/form.html', {
                'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
                    'footer' : True,
                    'titulo' : 'Usuarios',
                    'titulo_descripcion' : usr,
                    'frm' : frm
            } )
    else:
        frm = RegUsuario( instance = usr )
        return render( request, 'global/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
                'footer' : True,
                'titulo' : 'Usuarios',
                'titulo_descripcion' : usr,
                'frm' : frm
        } )

@valida_acceso( [ 'usr.eliminar_usuarios_usuario' ] )
def delete( request, pk ):
    Usr.objects.get( pk = pk ).delete()
    return HttpResponseRedirect( reverse( 'usuario_inicio' ) )
