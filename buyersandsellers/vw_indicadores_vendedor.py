from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import auth
import datetime

from seguridad.mkitsafe import *
from seguridad.models import *
from .models import *
from productos.models import *
from .vw_cliente import get_ctes_from_usr

@valida_acceso()
def index( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    actual = 0
    today = datetime.date.today()
    fecha_inicio = datetime.date( today.year - 1, today.month, 1 )
    if 2 == today.month:
        fecha_fin = datetime.date( today.year, today.month, 28 )
    elif today.month in [ 4, 6, 9, 11 ]:
        fecha_fin = datetime.date( today.year, today.month, 30 )
    else:
        fecha_fin = datetime.date( today.year, today.month, 31 )
    if "POST" == request.method:
        fecha_inicio = datetime.datetime.strptime( request.POST.get( 'fecha_inicio' ), '%Y-%m-%d' )
        fecha_fin = datetime.datetime.strptime( request.POST.get( 'fecha_fin' ), '%Y-%m-%d' )
        if "" != request.POST.get( 'idusrvendedor' ):
            actual = int( "0" + request.POST.get( 'idusrvendedor' ) )
            usr = Usr.objects.get( pk = actual )
            ctes = Vendedor.get_from_usr( usr ).clientes()
        else:
            ctes = get_ctes_from_usr( usuario )
    else:
        ctes = get_ctes_from_usr( usuario )
    graph_regs_vta = {}
    graph_regs_pago = {}
    for y in range( \
            int( "{:04d}{:02d}".format( fecha_inicio.year, fecha_inicio.month ) ), \
            int( "{:04d}{:02d}".format( fecha_fin.year, fecha_fin.month ) ) + 1 ):
        if 1 <= y % 100 and y % 100 <= 12:
            graph_regs_vta[ "{}-{:04.0f}".format( month_name( y % 100 ), y / 100 ) ] = { 
                'key' : "{}-{:04.0f}".format( month_name( y % 100 ), y / 100 ), 
                'value' : Decimal( 0.0 ) 
                }
            graph_regs_pago[ "{}-{:04.0f}".format( month_name( y % 100 ), y / 100 ) ] = { 
                'key' : "{}-{:04.0f}".format( month_name( y % 100 ), y / 100 ), 
                'value' : Decimal( 0.0 ) 
                }
    for cte in ctes:
        for vta in Cargo.objects.filter( cliente = cte, fecha__gte = fecha_inicio, fecha__lte = fecha_fin ):
            graph_regs_vta[ "{}-{:04d}".format( month_name( vta.fecha.month ), vta.fecha.year ) ][ 'value' ] += vta.monto
        for vta in Cargo.objects.filter( cliente = cte ):
            for pago in Abono.objects.filter( cargo = vta, fecha__gte = fecha_inicio, fecha__lte = fecha_fin ):
                graph_regs_pago[ "{}-{:04d}".format( month_name( pago.fecha.month ), pago.fecha.year ) ][ 'value' ] += pago.monto
    return render( 
        request, 
        'buyersandsellers/indicadores.html', 
        {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'fecha_inicio' : fecha_inicio,
            'fecha_fin' : fecha_fin,
            'req_ui' : requires_jquery_ui( request ),
            'encargados' : get_encardados( usuario ),
            'actual' : actual,
            'req_chart' : True,
            'graph_regs_vta' : procesa_graph_regs( graph_regs_vta ),
            'graph_regs_pago' : procesa_graph_regs( graph_regs_pago )
        } )

def get_encardados( usr ):
    usuario = usr
    if usuario.is_admin():
        gerentes = Vendedor.get_Gerentes()
        vendedores = Vendedor.get_Vendedores()
    elif usuario.depende_de is None and not Vendedor.get_from_usr( usuario ) is None:
        gerentes = [ Vendedor.get_from_usr( usuario ) ]
        vendedores = Vendedor.get_Vendedores( gerentes[ 0 ] )
    elif not Vendedor.get_from_usr( usuario ) is None:
        gerentes = []
        vendedores = [ Vendedor.get_from_usr( usuario ) ]
    else:
        gerentes = []
        vendedores = []
    return { 'gerentes' : gerentes, 'vendedores' : vendedores }

def procesa_graph_regs( graph_regs ):
    graph_regs = [ v for k, v in graph_regs.items() ]
    suma = Decimal( 0.0 )
    for k, reg in enumerate( graph_regs ):
        suma += reg[ 'value' ]
        if 0 == k:
            media = suma / 2
        else:
            media = suma / ( k + 1 )
        graph_regs[ k ][ 'media' ]=  media
    return graph_regs

