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

@valida_acceso( [ 'vendedor.vendedores_usuario' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'vendedor.agregar_vendedores_usuario' ):
        toolbar.append( { 'type' : 'link', 'view' : 'vendedor_nuevo', 'label' : '<i class="far fa-file"></i> Nuevo' } )
    data = []
    if usuario.is_admin():
        data = Vendedor.get_Vendedores()
    else:
        gerente = Vendedor.get_from_usr( usuario )
        if not gerente is None:
            data = Vendedor.get_Vendedores( gerente )
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
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if 'POST' == request.method:
        if usuario.is_admin():
            frm = RegVendedorInAdmin( request.POST, files = request.FILES )    
        else:
            frm = RegVendedorIn( request.POST, files = request.FILES )
        if frm.is_valid():
            perfil = Group.objects.get( name = '020 Vendedor' )
            usrdep = None
            obj = frm.save( commit = False )
            if not obj.reporta_a is None:
                usrdep = Usr.objects.get( pk = obj.reporta_a.idusuario )
            else:
                usrdep = usuario
                obj.reporta_a = Vendedor.get_from_usr( usuario )
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
            return HttpResponseRedirect( reverse( 'vendedor_ver', kwargs = { 'pk' : obj.pk } ) )
    if usuario.is_admin():
        frm = RegVendedorInAdmin( request.POST or None )    
    else:
        frm = RegVendedorIn( request.POST or None )
    return render( request, 'global/form.html', {
        'menu_main' : usuario.main_menu_struct(),
        'footer' : True,
        'titulo' : 'Vendedores',
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
    
@valida_acceso( [ 'vendedor.vendedores_usuario' ] )
def see( request, pk ):
    if not Vendedor.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    obj = Vendedor.objects.get( pk = pk )
    frm = RegVendedorAdmin( instance = obj )
    arbol = [ obj ] + obj.descendencia()
    for a in arbol:
        a = {
            'depth_name' : a.depth_name,
            'cliente' : a.groups.filter( name__icontains = 'Cliente' ).exists(),
            'vendedor' : a.groups.filter( name__icontains = 'Vendedor' ).exists()
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
    if not Vendedor.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    obj = Vendedor.objects.get( pk = pk )
    if 'POST' == request.method:
        if usuario.is_admin():
            frm = RegVendedorAdmin( instance = obj, data = request.POST, files = request.FILES )
        else:
            frm = RegVendedor( instance = obj, data = request.POST, files = request.FILES )
        if frm.is_valid():
            usrdep = None
            obj = frm.save( commit = False )
            if not obj.reporta_a is None:
                usrdep = Usr.objects.get( pk = obj.reporta_a.idusuario )
            else:
                usrdep = usuario
                obj.reporta_a = Vendedor.get_from_usr( usuario )
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
            return HttpResponseRedirect( reverse( 'vendedor_ver', kwargs = { 'pk' : obj.pk } ) )
        else:
            return render( request, 'global/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Vendedores',
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
    if usuario.is_admin():
        frm = RegVendedorAdmin( instance = obj, data = request.POST or None )
    else:
        frm = RegVendedor( instance = obj, data = request.POST or None )
    return render( request, 'global/form.html', {
        'menu_main' : usuario.main_menu_struct(),
        'footer' : True,
        'titulo' : 'Vendedores',
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

@valida_acceso( [ 'vendedor.eliminar_vendedores_usuario' ] )
def delete( request, pk ):
    try:
        if not Vendedor.objects.filter( pk = pk ).exists():
            return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
        Vendedor.objects.get( pk = pk ).delete()
        return HttpResponseRedirect( reverse( 'vendedor_inicio' ) )
    except ProtectedError:
        return HttpResponseRedirect( reverse( 'seguridad_item_con_relaciones' ) )
    