from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import auth
import decimal

from .forms import *
from .models import *
from .mkitsafe import *

# Agregado especifico por aplicacion
from random import shuffle
from productos.models import *

from django.conf import settings
from shutil import copyfile

# Create your views here.
@valida_acceso()
def index( request ):
    extra = None

    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    cte = usuario
    saldo = decimal.Decimal( 0 )
    for charge in Cargo.objects.filter( cliente = cte ):
        saldo += charge.saldo()
    mostrar_precio = 'f'
    productos = []
    if usuario.groups.filter( name__icontains = 'Cliente' ).exists():
        for c in Campaña.objects.filter( usuarios__in = [ usuario ], fecha_de_inicio__lte = date.today(), fecha_de_termino__gte = date.today() ):
            if c.mostrar_precio_de_venta:
                mostrar_precio = 't'
            prods2 = [ p for p in c.productos.filter( esta_activo = True ) if 0 == productos.count( p ) ]
            productos += prods2
        shuffle( productos )
        if len( productos ) < 6:
            prods2 = [ prod for prod in Producto.objects.filter( esta_activo = True ) ]
            shuffle( prods2 )
            productos = productos + prods2[ : 6 ]
    else:
        return HttpResponseRedirect( reverse( 'indicadores_inicio' ) )
    vendedor = None
    cte = Cliente.get_from_usr( cte )
    alias = ''
    txt_productos = ''
    wapp_vendedor = None
    if not cte is None:
        vendedor = cte.compra_a
        wapp_vendedor = vendedor.celular
        txt_productos = cte.texto_productos
        if "" != cte.alias and not cte.alias is None:
            alias = cte.alias
        else:
            alias = usuario.first_name
    return render( 
        request, 
        'seguridad_inicio.html', 
        {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : alias,
            # 'titulo_descripcion' : request.user.get_full_name(),
            'productos' : productos[ : 6 ],
            'mostrar_precio' : mostrar_precio,
            'saldo' : saldo,
            'vendedor' : vendedor,
            'txt_productos' : txt_productos,
            'wapp_vendedor' : wapp_vendedor,
            "extra": extra
        } )

def login( request ):
    frm = AccUsuario( request.POST or None )
    if frm.is_valid() and 'POST' == request.method:
        user = frm.login( request )
        if user is not None and user.is_active:
            auth.login( request, user )
            usuario = Usr.objects.get( id = user.pk )
            request.session[ 'usuario' ] = usuario.pk
            request.session[ 'usuario_pic' ] = "{}".format( usuario.fotografia )
            return HttpResponseRedirect( reverse( 'seguridad_inicio' ) )
    auth.logout( request )
    return render( 
        request, 
        'seguridad_login.html', {
        'footer' : True,
        'frm' : frm
    } )

def logout( request ):
    return HttpResponseRedirect( reverse( 'seguridad_login' ) )

@valida_acceso()
def item_not_found( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    return render(
        request,
        'seguridad_item_no_encontrado.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Elemento no encontrado'
        }
    )

@valida_acceso()
def item_with_relations( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    return render(
        request,
        'seguridad_item_con_relaciones.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Elemento relacionado'
        }
    )
