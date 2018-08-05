from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User

from seguridad.mkitsafe import *
from seguridad.models import Usr

from .forms import *

@valida_acceso( [ 'vendedor.vendedores_usuario' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'vendedor.agregar_vendedores_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'vendedor_nuevo', 'label' : '<i class="far fa-file"></i> Nuevo' } )
    data = []
    desc =  usuario.descendencia()
    for d in desc:
        if d.groups.filter( name = 'Vendedor' ).exists():
            data.append( Vendedor.objects.get( idusuario = d.pk ) )
    return render(
        request,
        'buyersandsellers/vendedor/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Vendedores',
            'data' : data,
            'toolbar' : toolbar
        } )
    
@valida_acceso( [ 'vendedor.agregar_vendedores_usuario' ] )
def new( request ):
    if 'POST' == request.method:
        frm = RegVendedorIn( request.POST, files = request.FILES )
        if frm.is_valid():
            perfil = Group.objects.get( name = 'Vendedor' )
            usrdep = None
            obj = frm.save( commit = False )
            if not obj.reporta_a is None:
                usrdep = Usr.objects.get( pk = obj.reporta_a.idusuario )
            obj.username = obj.usuario
            obj.set_password( obj.contraseña )
            obj.save()
            obj.groups.add( perfil )
            obj.depende_de = usrdep
            obj.save()
            return HttpResponseRedirect( reverse( 'vendedor_ver', kwargs = { 'pk' : obj.pk } ) )
    frm = RegVendedorIn( request.POST or None )
    return render( request, 'global/form.html', {
        'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
        'footer' : True,
        'titulo' : 'Vendedores',
        'titulo_descripcion' : 'Nuevo',
        'frm' : frm
    } )
    
@valida_acceso( [ 'vendedor.vendedores_usuario' ] )
def see( request, pk ):
    obj = Vendedor.objects.get( pk = pk )
    frm = RegVendedor( instance = obj )
    arbol = [ obj ] + obj.descendencia()
    for a in arbol:
        a = {
            'depth_name' : a.depth_name,
            'cliente' : a.groups.filter( name = 'Cliente' ).exists(),
            'vendedor' : a.groups.filter( name = 'Vendedor' ).exists()
        }
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'vendedor.vendedores_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'vendedor_inicio', 'label' : '<i class="fas fa-list-ul"></i> Ver todos' } )
    if usuario.has_perm_or_has_perm_child( 'vendedor.actualizar_vendedores_usuario' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'vendedor_actualizar', 'label' : '<i class="far fa-edit"></i> Actualizar', 'pk' : pk } )
    if usuario.has_perm_or_has_perm_child( 'vendedor.eliminar_vendedores_usuario' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'vendedor_eliminar', 'label' : '<i class="far fa-trash-alt"></i> Eliminar', 'pk' : pk } )
    return render( request, 'buyersandsellers/vendedor/see.html', {
        'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Vendedores',
            'titulo_descripcion' : obj,
            'read_only' : True,
            'frm' : frm,
            'fotografia' : obj.fotografia,
            'toolbar' : toolbar,
            'arbol' : arbol
    } )
    
@valida_acceso( [ 'vendedor.actualizar_vendedores_usuario' ] )
def update( request, pk ):
    obj = Vendedor.objects.get( pk = pk )
    if 'POST' == request.method:
        frm = RegVendedor( instance = obj, data = request.POST, files = request.FILES )
        if frm.is_valid():
            usrdep = None
            obj = frm.save( commit = False )
            if not obj.reporta_a is None:
                usrdep = Usr.objects.get( pk = obj.reporta_a.idusuario )
            obj.username = obj.usuario
            obj.save()
            obj.depende_de = usrdep
            obj.save()
            return HttpResponseRedirect( reverse( 'vendedor_ver', kwargs = { 'pk' : obj.pk } ) )
        else:
            return render( request, 'global/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Vendedores',
            'titulo_descripcion' : obj,
            'frm' : frm
        } )
    frm = RegVendedor( instance = obj )
    return render( request, 'global/form.html', {
        'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
        'footer' : True,
        'titulo' : 'Vendedores',
        'titulo_descripcion' : obj,
        'frm' : frm
    } )


@valida_acceso( [ 'vendedor.eliminar_vendedores_usuario' ] )
def delete( request, pk ):
    Vendedor.objects.get( pk = pk ).delete()
    return HttpResponseRedirect( reverse( 'vendedor_inicio' ) )
    