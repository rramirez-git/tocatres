from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
from operator import attrgetter
import json
import decimal

from .models import *
from seguridad.mkitsafe import *
from tocatres.utils import requires_jquery_ui

@valida_acceso( [ 'cargo.ventas_y_pagos_cargo' ] )
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if 'POST' == request.method:
        cte = Usr.objects.get( pk = request.POST.get( 'cte' ) )
        if 'addcharge' == request.POST.get( 'action' ):
            prod = Producto.objects.get( pk = request.POST.get( 'product' ) )
            Cargo.objects.create(
                fecha = request.POST.get( 'fecha_cargo' ),
                factura = request.POST.get( 'factura' ),
                concepto = request.POST.get( 'concepto_cargo' ),
                monto = request.POST.get( 'monto_cargo' ),
                producto = prod,
                cliente = cte,
                vendedor = usuario
            )
        elif 'addpayment' == request.POST.get( 'action' ):
            cargo = Cargo.objects.get( pk = request.POST.get( 'cargo' ) )
            Abono.objects.create(
                fecha = request.POST.get( 'fecha_abono' ),
                no_de_pago = request.POST.get( 'no_de_pago' ),
                concepto = request.POST.get( 'concepto_abono' ),
                monto = request.POST.get( 'monto_abono' ),
                cargo = cargo,
                vendedor = usuario
            )
            cargo.actualizable = False
            if cargo.saldo() <= 0:
                cargo.saldado = True
            cargo.save()
            if cargo.saldado:
                for abono in Abono.objects.filter( cargo = cargo ):
                    abono.actualizable = False
                    abono.save()
        return HttpResponseRedirect( reverse( 'cargos_abonos_edocta', kwargs = { 'pk' : cte.pk } ) )
    my_clients = []
    all_clients = []
    if usuario.groups.all().filter( name__icontains = 'Administrador' ).exists() \
            or usuario.groups.all().filter( name__icontains = 'Super-Administrador' ).exists() \
            or usuario.is_superuser:
        desc = Usr.objects.all()
    else:
        desc = usuario.descendencia()
    for u in desc:
        if u.groups.all().filter( name__icontains = 'Cliente' ).exists() and u.is_active:
            if u.depende_de == usuario:
                my_clients.append( u )
            else:
                all_clients.append( u )
    return render( 
        request, 
        'productos/cargos-abonos/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Movimientos',
            'my_clients' : sorted( my_clients, key = attrgetter( 'first_name', 'last_name' ) ),
            'all_clients' : sorted( all_clients, key = attrgetter( 'first_name', 'last_name' ) ),
            'products' : Producto.objects.filter( esta_activo = True ),
            'req_ui' : requires_jquery_ui( request )
    } )

@valida_acceso( [ 'cargo.ventas_y_pagos_cargo' ] )
def account( request, pk ):
    if not Usr.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    cte = Usr.objects.get( pk = pk )
    charges = Cargo.objects.filter( cliente = cte )
    movs = []
    saldo = decimal.Decimal( 0 )
    for charge in charges:
        movs.append( charge )
        saldo += charge.saldo()
        for payment in Abono.objects.filter( cargo = charge ):
            movs.append( payment )
    sorted( movs, key = attrgetter( 'fecha', 'concepto' ) )
    movs.reverse()
    return render( request, 'productos/cargos-abonos/edo-cta.html', {
        'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Estado de Cuenta',
            'titulo_descripcion' : cte,
            'movs' : movs,
            'saldo' : saldo,
            'cte' : cte
    } )

@valida_acceso( [ 'cargo.ventas_y_pagos_cargo' ] )
def getcargos( request, pk ):
    cte = Usr.objects.get( pk = pk )
    json_movs = { 'charges' : [], 'no_abono' : 1  }
    movs =  Cargo.objects.filter( cliente = cte ).order_by( 'factura', 'concepto' )
    for mov in movs:
        json_movs[ 'charges' ].append( {
            'id' : "{}".format( mov.idcargo ),
            'monto' : "{}".format( mov.monto ),
            'saldo' : "{}".format( mov.saldo() ),
            'cargo' : "{}".format( mov )
        } )
        json_movs[ 'no_abono' ] += mov.no_abonos()
    return HttpResponse( json.dumps( json_movs ), content_type = 'application/json' )

@valida_acceso( [ 'cargo.remover_cargo_cargo' ] )
def delete_cargo( request, pk, pkcte ):
    obj =  Cargo.objects.get( pk = pk )
    if obj.actualizable:
        obj.delete()
    return HttpResponseRedirect( reverse( 'cargos_abonos_edocta', kwargs = { 'pk' : pkcte } ) )

@valida_acceso( [ 'abono.remover_abono_abono'] )
def delete_abono( request, pk, pkcte ):
    obj =  Abono.objects.get( pk = pk )
    cargo = obj.cargo
    if obj.actualizable:
        obj.delete()
    if 0 <= cargo.saldo():
        cargo.saldado = True
    else:
        cargo.saldado = False
    if not Abono.objects.filter( cargo = cargo ).exists():
        cargo.actualizable = True
    cargo.save()
    return HttpResponseRedirect( reverse( 'cargos_abonos_edocta', kwargs = { 'pk' : pkcte } ) )

@valida_acceso( [ 'permission.mi_saldo_permiso' ] )
def mi_saldo( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    cte = usuario
    charges = Cargo.objects.filter( cliente = cte )
    movs = []
    saldo = decimal.Decimal( 0 )
    for charge in charges:
        movs.append( charge )
        saldo += charge.saldo()
        for payment in Abono.objects.filter( cargo = charge ):
            movs.append( payment )
    sorted( movs, key = attrgetter( 'fecha', 'concepto' ) )
    movs.reverse()
    vendedor = None
    cte = Cliente.get_from_usr( usuario )
    if not cte is None:
        vendedor = cte.compra_a
    return render( request, 'productos/cargos-abonos/mi-saldo.html', {
        'menu_main' : usuario.main_menu_struct(),
        'footer' : True,
        'titulo' : None,
        'movs' : movs[ : 15 ],
        'saldo' : saldo
    } )