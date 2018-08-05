from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User

from seguridad.mkitsafe import *
from seguridad.models import Usr

from .forms import *

@valida_acceso( [ 'cliente.clientes_usuario' ] )
def index( request ):
    data = []
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'cliente.agregar_clientes_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'cliente_nuevo', 'label' : '<i class="far fa-file"></i> Nuevo' } )
    if usuario.is_superuser:
        data = Cliente.objects.all()
    elif usuario.groups.filter( name = 'Vendedor' ).exists():
        for cte in Vendedor.objects.get( idusuario = usuario.pk ).all_clientes():
            data.append( cte )
    return render(
        request,
        'buyersandsellers/cliente/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Clientes',
            'data' : data,
            'toolbar' : toolbar
        } )
    
@valida_acceso( [ 'cliente.agregar_clientes_usuario' ] )
def new( request ):
    if 'POST' == request.method:
        frm = RegClienteIn( request.POST, files = request.FILES )
        if frm.is_valid():
            perfil = Group.objects.get( name = 'Cliente' )
            obj = frm.save( commit = False )
            usrdep = Usr.objects.get( pk = obj.compra_a.idusuario )
            obj.username = obj.usuario
            obj.set_password( obj.contraseña )
            obj.save()
            obj.groups.add( perfil )
            obj.depende_de = usrdep
            obj.save()
            return HttpResponseRedirect( reverse( 'cliente_ver', kwargs = { 'pk' : obj.pk } ) )
    frm = RegClienteIn( request.POST or None )
    return render( request, 'global/form.html', {
        'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
        'footer' : True,
        'titulo' : 'Clientes',
        'titulo_descripcion' : 'Nuevo',
        'frm' : frm
    } )
    
@valida_acceso( [ 'cliente.clientes_usuario' ] )
def see( request, pk ):
    obj = Cliente.objects.get( pk = pk )
    frm = RegCliente( instance = obj )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'cliente.clientes_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'cliente_inicio', 'label' : '<i class="fas fa-list-ul"></i> Ver todos' } )
    if usuario.has_perm_or_has_perm_child( 'cliente.actualizar_clientes_usuario' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'cliente_actualizar', 'label' : '<i class="far fa-edit"></i> Actualizar', 'pk' : pk } )
    if usuario.has_perm_or_has_perm_child( 'cliente.eliminar_clientes_usuario' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'cliente_eliminar', 'label' : '<i class="far fa-trash-alt"></i> Eliminar', 'pk' : pk } )
    return render( request, 'seguridad/usuario/see.html', {
        'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Clientes',
            'titulo_descripcion' : obj,
            'read_only' : True,
            'frm' : frm,
            'fotografia' : obj.fotografia,
            'toolbar' : toolbar
    } )
    
@valida_acceso( [ 'cliente.actualizar_clientes_usuario' ] )
def update( request, pk ):
    obj = Cliente.objects.get( pk = pk)
    if 'POST' == request.method:
        frm = RegCliente( instance = obj, data = request.POST, files = request.FILES )
        if frm.is_valid():
            obj = frm.save( commit = False )
            usrdep = Usr.objects.get( pk = obj.compra_a.idusuario )
            obj.username = obj.usuario
            obj.save()
            obj.depende_de = usrdep
            obj.save()
            return HttpResponseRedirect( reverse( 'cliente_ver', kwargs = { 'pk' : obj.pk } ) )
        else:
            return render( request, 'global/form.html', {
                'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
                'footer' : True,
                'titulo' : 'Clientes',
                'titulo_descripcion' : obj,
                'frm' : frm
            } )
    else:
        frm = RegCliente( instance = obj )
        return render( request, 'global/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Clientes',
            'titulo_descripcion' : 'Nuevo',
            'frm' : frm
        } )

@valida_acceso( [ 'cliente.eliminar_clientes_usuario' ] )
def delete( request, pk ):
    Cliente.objects.get( pk = pk ).delete()
    return HttpResponseRedirect( reverse( 'cliente_inicio' ) )
    