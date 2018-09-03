from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.db.models import ProtectedError
from django.conf import settings
from random import randint
from os.path import isfile
from os import remove

from operator import attrgetter

from seguridad.mkitsafe import *
from seguridad.models import Usr

from .forms import *

@valida_acceso( [ 'cliente.clientes_usuario' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'cliente.agregar_clientes_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'cliente_nuevo', 'label' : '<i class="far fa-file"></i> Nuevo' } )
    data = get_ctes_from_usr( usuario )
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
            perfil = Group.objects.get( name = '010 Cliente' )
            obj = frm.save( commit = False )
            usrdep = Usr.objects.get( pk = obj.compra_a.idusuario )
            obj.username = obj.usuario
            obj.set_password( obj.contraseña )
            obj.save()
            obj.groups.add( perfil )
            obj.depende_de = usrdep
            obj.save()
            upload_to = 'usuarios'
            if "" != request.POST.get( 'token' ):
                file = "{}{}/{}.imgx".format( settings.MEDIA_ROOT, upload_to, request.POST.get( 'token' ) )
                if isfile( file ):
                    f = open( file, "r" )
                    if "r" == f.mode:
                        img = f.read().strip()
                        f.close()
                        obj.fotografia = "{}/{}".format( upload_to, img )
                        obj.save()
                        remove( file )
            return HttpResponseRedirect( reverse( 'cliente_ver', kwargs = { 'pk' : obj.pk } ) )
    frm = RegClienteIn( request.POST or None )
    return render( request, 'global/form.html', {
        'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
        'footer' : True,
        'titulo' : 'Clientes',
        'titulo_descripcion' : 'Nuevo',
        'frm' : frm,
        'uploader' : {
            'url' : settings.UPLOADER_URL,
            'site' : settings.UPLOADER_SITE,
            'key' : settings.UPLOADER_KEY,
            'onresponse' : '',
            'type' : 'usuarios',
            'excecute' : '',
            'token' : randint( 1, 999999999 ),
            'message' : "Archivo Cargado",
        }
    } )
    
@valida_acceso( [ 'cliente.clientes_usuario' ] )
def see( request, pk ):
    if not Cliente.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
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
    if not Cliente.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
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
            upload_to = 'usuarios'
            if "" != request.POST.get( 'token' ):
                file = "{}{}/{}.imgx".format( settings.MEDIA_ROOT, upload_to, request.POST.get( 'token' ) )
                if isfile( file ):
                    f = open( file, "r" )
                    if "r" == f.mode:
                        img = f.read().strip()
                        f.close()
                        obj.fotografia = "{}/{}".format( upload_to, img )
                        obj.save()
                        remove( file )
            return HttpResponseRedirect( reverse( 'cliente_ver', kwargs = { 'pk' : obj.pk } ) )
        else:
            return render( request, 'global/form.html', {
                'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
                'footer' : True,
                'titulo' : 'Clientes',
                'titulo_descripcion' : obj,
                'frm' : frm,
                'uploader' : {
                    'url' : settings.UPLOADER_URL,
                    'site' : settings.UPLOADER_SITE,
                    'key' : settings.UPLOADER_KEY,
                    'onresponse' : '',
                    'type' : 'usuarios',
                    'excecute' : '',
                    'token' : randint( 1, 999999999 ),
                    'message' : "Archivo Cargado",
                }
            } )
    else:
        frm = RegCliente( instance = obj )
        return render( request, 'global/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Clientes',
            'titulo_descripcion' : obj,
            'frm' : frm,
            'uploader' : {
                'url' : settings.UPLOADER_URL,
                'site' : settings.UPLOADER_SITE,
                'key' : settings.UPLOADER_KEY,
                'onresponse' : '',
                'type' : 'usuarios',
                'excecute' : '',
                'token' : randint( 1, 999999999 ),
                'message' : "Archivo Cargado",
            }
        } )

@valida_acceso( [ 'cliente.eliminar_clientes_usuario' ] )
def delete( request, pk ):
    try:
        if not Cliente.objects.filter( pk = pk ).exists():
            return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
        Cliente.objects.get( pk = pk ).delete()
        return HttpResponseRedirect( reverse( 'cliente_inicio' ) )
    except ProtectedError:
        return HttpResponseRedirect( reverse( 'seguridad_item_con_relaciones' ) )
    
def get_ctes_from_usr( usuario ):
    data = []
    if usuario.is_superuser \
            or usuario.groups.filter( name__icontains = "Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Super-Administrador" ).exists():
        for gerente in Vendedor.get_Gerentes():
            for cte in gerente.all_clientes():
                data.append( cte )
    else:
        vendedor = Vendedor.get_from_usr( usuario )
        if not vendedor is None:
            for cte in vendedor.all_clientes():
                data.append( cte )
    decorado = [ ( tmpusr.compra_a, i, tmpusr ) for i, tmpusr in enumerate( data ) ]
    decorado.sort()
    data = [ tmpusr for compra_a, i, tmpusr in decorado ]
    return data