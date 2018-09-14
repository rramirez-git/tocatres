from django.shortcuts import render
from django.db.models import ProtectedError, Q
from django.conf import settings
from random import randint
from os.path import isfile
from os import remove

from .forms import *
from .models import *
from seguridad.mkitsafe import *

@valida_acceso( [ 'producto.administrar_productos_producto' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if "POST" == request.method:
        for prod in Producto.objects.filter( Q( pk__in = request.POST.getlist( 'producto_activo_id' ) ) ):
            prod.esta_activo = True
            prod.save()
        for prod in Producto.objects.filter( ~Q( pk__in = request.POST.getlist( 'producto_activo_id' ) ) ):
            prod.esta_activo = False
            prod.save()
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'producto.agregar_productos_producto' ):
        toolbar.append( { 'type' : 'link', 'view' : 'producto_nuevo', 'label' : '<i class="far fa-file"></i> Nuevo' } )
    return render(
        request,
        'productos/producto/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Productos',
            'data' : Producto.objects.all(),
            'toolbar' : toolbar
        } )

@valida_acceso( [ 'producto.agregar_productos_producto' ] )
def new( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if 'POST' == request.method:
        if usuario.has_perm_or_has_perm_child( 'producto.administrar_precios_producto' ):
            frm = RegProductoCPrecio( request.POST, files = request.FILES )
        else:
            frm = RegProducto( request.POST, files = request.FILES )
        if frm.is_valid():
            obj = frm.save()
            upload_to = 'productos'
            if "" != request.POST.get( 'token' ):
                file = "{}{}/{}.imgx".format( settings.MEDIA_ROOT, upload_to, request.POST.get( 'token' ) )
                if isfile( file ):
                    f = open( file, "r" )
                    if "r" == f.mode:
                        img = f.read().strip()
                        f.close()
                        obj.imagen = "{}/{}".format( upload_to, img )
                        obj.save()
                        remove( file )
            return HttpResponseRedirect( reverse( 'producto_ver', kwargs = { 'pk' : obj.pk } ) )
    if usuario.has_perm_or_has_perm_child( 'producto.administrar_precios_producto' ):
        frm = RegProductoCPrecio( request.POST or None )
    else:
        frm = RegProducto( request.POST or None )
    return render( request, 'global/form.html', {
        'menu_main' : usuario.main_menu_struct(),
        'footer' : True,
        'titulo' : 'Productos',
        'titulo_descripcion' : 'Nuevo',
        'action' : 'producto_nuevo',
        'frm' : frm,
        'uploader' : {
            'url' : settings.UPLOADER_URL,
            'site' : settings.UPLOADER_SITE,
            'key' : settings.UPLOADER_KEY,
            'onresponse' : '',
            'type' : 'productos',
            'excecute' : '',
            'token' : randint( 1, 999999999 ),
            'message' : "Archivo Cargado",
        }
    } )

@valida_acceso( [ 'producto.administrar_productos_producto' ] )
def see( request, pk ):
    if not Producto.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    obj = Producto.objects.get( pk = pk )
    if usuario.has_perm_or_has_perm_child( 'producto.administrar_precios_producto' ):
        frm = RegProductoCPrecio( instance = obj )
    else:
        frm = RegProducto( instance = obj )
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'producto.administrar_productos_producto' ):
        toolbar.append( { 'type' : 'link', 'view' : 'producto_inicio', 'label' : '<i class="fas fa-list-ul"></i> Ver todos' } )
    if usuario.has_perm_or_has_perm_child( 'producto.actualizar_productos_producto' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'producto_actualizar', 'label' : '<i class="far fa-edit"></i> Actualizar', 'pk' : pk } )
    if usuario.has_perm_or_has_perm_child( 'producto.eliminar_productos_producto' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'producto_eliminar', 'label' : '<i class="far fa-trash-alt"></i> Eliminar', 'pk' : pk } )
    return render( request, 'productos/producto/see.html', {
        'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Productos',
            'titulo_descripcion' : obj,
            'read_only' : True,
            'frm' : frm,
            'fotografia' : obj.imagen,
            'toolbar' : toolbar
    } )

@valida_acceso( [ 'producto.actualizar_productos_producto' ] )
def update( request, pk ):
    if not Producto.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    obj = Producto.objects.get( pk = pk )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if 'POST' == request.method:
        if usuario.has_perm_or_has_perm_child( 'producto.administrar_precios_producto' ):
            frm = RegProductoCPrecio( instance = obj, data = request.POST, files = request.FILES )
        else:
            frm = RegProducto( instance = obj, data = request.POST, files = request.FILES )
        if frm.is_valid():
            obj = frm.save()
            upload_to = 'productos'
            if "" != request.POST.get( 'token' ):
                file = "{}{}/{}.imgx".format( settings.MEDIA_ROOT, upload_to, request.POST.get( 'token' ) )
                if isfile( file ):
                    f = open( file, "r" )
                    if "r" == f.mode:
                        img = f.read().strip()
                        f.close()
                        obj.imagen = "{}/{}".format( upload_to, img )
                        obj.save()
                        remove( file )
            return HttpResponseRedirect( reverse( 'producto_ver', kwargs = { 'pk' : obj.pk } ) )
        else:
            return render( request, 'global/form.html', {
                'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
                'footer' : True,
                'titulo' : 'Productos',
                'titulo_descripcion' : obj,
                'frm' : frm,
                'uploader' : {
                    'url' : settings.UPLOADER_URL,
                    'site' : settings.UPLOADER_SITE,
                    'key' : settings.UPLOADER_KEY,
                    'onresponse' : '',
                    'type' : 'productos',
                    'excecute' : '',
                    'token' : randint( 1, 999999999 ),
                    'message' : "Archivo Cargado",
                }
            } )
    else:
        if usuario.has_perm_or_has_perm_child( 'producto.administrar_precios_producto' ):
            frm = RegProductoCPrecio( instance = obj )
        else:
            frm = RegProducto( instance = obj )
        return render( request, 'global/form.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Productos',
            'titulo_descripcion' : obj,
            'frm' : frm,
            'uploader' : {
                'url' : settings.UPLOADER_URL,
                'site' : settings.UPLOADER_SITE,
                'key' : settings.UPLOADER_KEY,
                'onresponse' : '',
                'type' : 'productos',
                'excecute' : '',
                'token' : randint( 1, 999999999 ),
                'message' : "Archivo Cargado",
            }
        } )

@valida_acceso( [ 'producto.eliminar_productos_producto' ] )
def delete( request, pk ):
    try:
        if not Producto.objects.filter( pk = pk ).exists():
            return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
        Producto.objects.get( pk = pk ).delete()
        return HttpResponseRedirect( reverse( 'producto_inicio' ) )
    except ProtectedError:
        return HttpResponseRedirect( reverse( 'seguridad_item_con_relaciones' ) )

@valida_acceso( [ 'campaña.novedades_campaña' ] )
def detalle( request, pk, mp ):
    if not Producto.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    obj = Producto.objects.get( pk = pk )
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'campaña.novedades_campaña' ):
        toolbar.append( { 'type' : 'link', 'view' : 'campaña_novedades', 'label' : '<i class="fas fa-glasses"></i> Ver Catálogo' } )
    vendedor = None
    cte = Cliente.get_from_usr( usuario )
    if not cte is None:
        vendedor = cte.compra_a
    mensaje_whats = 'Hola, solicitando información del producto *{}* (SKU: _{}_)'.format( obj.nombre, obj.sku )
    return render( request, 'productos/producto/detalle.html', {
        'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : obj,
            'titulo_descripcion' : "SKU: " + obj.sku,
            'read_only' : True,
            'prod' : obj,
            'fotografia' : obj.imagen,
            'toolbar' : toolbar,
            'mostrar_precio' : mp,
            'vendedor' : vendedor,
            'mensaje_whats' : mensaje_whats
    } )