from django.shortcuts import render
from django.db.models import ProtectedError
from datetime import date
from random import shuffle

from .forms import *
from .models import *
from seguridad.mkitsafe import *
from tocatres.utils import requires_jquery_ui

@valida_acceso( [ 'campaña.campanas_campaña' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'campaña.agregar_campanas_campaña' ):
        toolbar.append( { 'type' : 'link', 'view' : 'campaña_nuevo', 'label' : '<i class="far fa-file"></i> Nueva' } )
    if usuario.has_perm_or_has_perm_child( 'campaña.asignar_campanas_campaña' ):
        toolbar.append( { 'type' : 'link', 'view' : 'campaña_asignar', 'label' : '<i class="fas fa-users"></i> Asignar' } )
    return render(
        request,
        'productos/campania/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Campañas',
            'data' : Campaña.objects.all().order_by( '-fecha_de_inicio', '-fecha_de_termino', 'nombre' ),
            'toolbar' : toolbar
        } )

@valida_acceso( [ 'campaña.agregar_campanas_campaña' ] )
def new( request ):
    frm = RegCampaña( request.POST or None )
    if 'POST' == request.method:
        if frm.is_valid():
            obj = frm.save()
            return HttpResponseRedirect( reverse( 'campaña_ver', kwargs = { 'pk' : obj.pk } ) )
    return render( request, 'global/form.html', {
        'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
        'footer' : True,
        'titulo' : 'Campañas',
        'titulo_descripcion' : 'Nueva',
        'frm' : frm,
        'req_ui' : requires_jquery_ui( request )
    } )

@valida_acceso( [ 'campaña.campanas_campaña' ] )
def see( request, pk ):
    if not Campaña.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    obj = Campaña.objects.get( pk = pk )
    frm = RegCampaña( instance = obj )
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'campaña.campanas_campaña' ):
        toolbar.append( { 'type' : 'link', 'view' : 'campaña_inicio', 'label' : '<i class="fas fa-list-ul"></i> Ver todas' } )
    if usuario.has_perm_or_has_perm_child( 'campaña.actualizar_campanas_campaña' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'campaña_actualizar', 'label' : '<i class="far fa-edit"></i> Actualizar', 'pk' : pk } )
    if usuario.has_perm_or_has_perm_child( 'campaña.eliminar_campanas_campaña' ):
        toolbar.append( { 'type' : 'link_pk', 'view' : 'campaña_eliminar', 'label' : '<i class="far fa-trash-alt"></i> Eliminar', 'pk' : pk } )
    return render( request, 'global/form.html', {
        'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Campañas',
            'titulo_descripcion' : obj,
            'read_only' : True,
            'frm' : frm,
            'toolbar' : toolbar
    } )

@valida_acceso( [ 'campaña.actualizar_campanas_campaña' ] )
def update( request, pk ):
    if not Campaña.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    obj = Campaña.objects.get( pk = pk)
    if 'POST' == request.method:
        frm = RegCampaña( instance = obj, data = request.POST, files = request.FILES )
        if frm.is_valid():
            obj = frm.save()
            return HttpResponseRedirect( reverse( 'campaña_ver', kwargs = { 'pk' : obj.pk } ) )
        else:
            return render( request, 'global/form.html', {
                'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
                'footer' : True,
                'titulo' : 'Campañas',
                'titulo_descripcion' : obj,
                'frm' : frm,
            'req_ui' : requires_jquery_ui( request )
            } )
    else:
        frm = RegCampaña( instance = obj )
        return render( request, 'global/form.html', {
            'menu_main' : Usr.objects.filter( id = request.user.pk )[ 0 ].main_menu_struct(),
            'footer' : True,
            'titulo' : 'Campañas',
            'titulo_descripcion' : obj,
            'frm' : frm,
            'req_ui' : requires_jquery_ui( request )
        } )

@valida_acceso( [ 'campaña.eliminar_campanas_campaña' ] )
def delete( request, pk ):
    try:
        if not Campaña.objects.filter( pk = pk ).exists():
            return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
        Campaña.objects.get( pk = pk ).delete()
        return HttpResponseRedirect( reverse( 'campaña_inicio' ) )
    except ProtectedError:
        return HttpResponseRedirect( reverse( 'seguridad_item_con_relaciones' ) )

@valida_acceso( [ 'campaña.asignar_campanas_campaña' ] )
def assign( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    msg = None
    if 'POST' == request.method:
        mc = request.POST.getlist( 'misclientes' )
        mv = request.POST.getlist( 'misvendedores' )
        ctes = request.POST.getlist( 'clientes' )
        campaña = Campaña.objects.get( pk = request.POST.get( 'campaign' ) )
        if 'yes' == request.POST.get( 'eliminar_anteriores' ):
            campaña.usuarios.clear()
        for cte in mc:
            usr = Usr.objects.get( pk = cte )
            campaña.usuarios.add( usr )
        for cte in ctes:
            usr = Usr.objects.get( pk = cte )
            campaña.usuarios.add( usr )
        for vend in mv:
            v = Usr.objects.get( pk = vend )
            for cte in v.hijos():
                if cte.groups.all().filter( name__icontains = 'Cliente' ).exists():
                    campaña.usuarios.add( cte )
        campaña.save()
        msg = "Campaña Asignada correctamente."
    data = { 'misclientes' : [], 'misvendedores' : [], 'clientes' : [] }
    if usuario.groups.all().filter( name__icontains = 'Administrador' ).exists() \
            or usuario.groups.all().filter( name__icontains = 'Super-Administrador' ).exists() \
            or usuario.is_superuser:
        desc = Usr.objects.all()
    else:
        desc = usuario.descendencia()
    for u in desc:
        if u.groups.all().filter( name__icontains = 'Vendedor' ).exists():
            data[ 'misvendedores' ].append( u )
        if u.groups.all().filter( name__icontains = 'Cliente' ).exists():
            data[ 'clientes' ].append( u )
            if u.depende_de == usuario:
                data[ 'misclientes' ].append( u )
    return render( request, 'productos/campania/assign.html', {
        'menu_main' : usuario.main_menu_struct(),
        'footer' : True,
        'titulo' : 'Campañas',
        'titulo_descripcion' : 'Asignar',
        'data':  data,
        'campaigns' : Campaña.objects.all(),
        'msg' : msg
    } )

@valida_acceso( [ 'campaña.novedades_campaña' ] )
def novedades( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    mostrar_precio = 'f'
    productos = []
    # for c in Campaña.objects.filter( usuarios__in = [ usuario ], fecha_de_inicio__lte = date.today(), fecha_de_termino__gte = date.today() ):
    #     if c.mostrar_precio_de_venta:
    #         mostrar_precio = 't'
    #     for p in c.productos.all():
    #         if 0 == productos.count( p ):
    #             productos.append( p )
    for p in Producto.objects.all():
        productos.append( p )
    #shuffle( productos )
    return render( request, 'productos/campania/novedades.html', {
        'menu_main' : usuario.main_menu_struct(),
        'footer' : True,
        'titulo' : None,
        'mostrar_precio' : 't',
        'productos' : productos
    } )

