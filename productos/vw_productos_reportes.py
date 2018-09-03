from django.shortcuts import render

from decimal import Decimal
import datetime

from .models import *

from seguridad.mkitsafe import *
from buyersandsellers.vw_cliente import get_ctes_from_usr
from tocatres.utils import requires_jquery_ui, month_name

@valida_acceso( [ 'abono.saldos_abono' ] )
def saldos( request ):
    show_vendedor = False
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if usuario.is_superuser \
            or usuario.groups.filter( name__icontains = "Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Super-Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Gerente" ).exists():
        show_vendedor = True
    actual = 0
    if "POST" == request.method and "" != request.POST.get( 'idusrvendedor' ):
        actual = int( "0" + request.POST.get( 'idusrvendedor' ) )
        usr = Usr.objects.get( pk = actual )
        ctes = Vendedor.get_from_usr( usr ).clientes()
    else:
        ctes = get_ctes_from_usr( usuario )
    data = []
    totales = { 
        'ventas' : Decimal( 0.0 ), 
        'pagos' : Decimal( 0.0 ), 
        'saldo' : Decimal( 0.0 ), 
        'recuperacion' : Decimal( 0.0 ) 
    }
    for cte in ctes:
        ventas = Decimal( 0.0 )
        saldo = Decimal( 0.0 )
        fecha = datetime.date( 2000, 1, 1 )
        for vta in Cargo.objects.filter( cliente = cte ):
            ventas += vta.monto
            saldo += vta.saldo()
            for pago in Abono.objects.filter( cargo = vta, fecha__gte = fecha ):
                if fecha < pago.fecha:
                    fecha = pago.fecha
        if datetime.date( 2000, 1, 1 ) == fecha:
            fecha = "Sin Pagos"
        pagos = ventas - saldo
        totales[ 'ventas' ] += ventas
        totales[ 'pagos' ] += pagos
        totales[ 'saldo' ] += saldo
        data.append( {
            'idcte'     : cte.pk,
            'idusrcte'  : cte.idusuario,
            'cte'       : "{}".format( cte ),
            'idvend'    : cte.compra_a.pk,
            'vend'      : "{}".format( cte.compra_a ),
            'ventas'    : ventas,
            'pagos'     : pagos,
            'saldo'     : saldo,
            'fecha'     : fecha
        } )
    totales[ 'recuperacion' ] = "{:02.2f}".format( totales[ 'pagos' ] * Decimal( 100.0 ) / totales[ 'ventas' ] )
    return render(
        request,
        'productos/reportes/saldos.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Reporte de Saldos',
            'data' : data,
            'show_vendedor' : show_vendedor,
            'totales' : totales,
            'encargados' : get_encardados( usuario ),
            'actual' : actual
        } )

@valida_acceso( [ 'abono.ventas_abono' ] )
def ventas( request ):
    show_vendedor = False
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if usuario.is_superuser \
            or usuario.groups.filter( name__icontains = "Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Super-Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Gerente" ).exists():
        show_vendedor = True
    actual = 0
    data = []
    totales = { 'ventas' : Decimal( 0.0 ) }
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
    graph_regs = {}
    for y in range( \
            int( "{:04d}{:02d}".format( fecha_inicio.year, fecha_inicio.month ) ), \
            int( "{:04d}{:02d}".format( fecha_fin.year, fecha_fin.month ) ) + 1 ):
        if 1 <= y % 100 and y % 100 <= 12:
            graph_regs[ "{}-{:04.0f}".format( month_name( y % 100 ), y / 100 ) ] = { 
                'key' : "{}-{:04.0f}".format( month_name( y % 100 ), y / 100 ), 
                'value' : Decimal( 0.0 ) 
                }
    for cte in ctes:
        ventas = Decimal( 0.0 )
        fecha = datetime.date( 2000, 1, 1 )
        for vta in Cargo.objects.filter( cliente = cte, fecha__gte = fecha_inicio, fecha__lte = fecha_fin ):
            ventas += vta.monto
            graph_regs[ "{}-{:04d}".format( month_name( vta.fecha.month ), vta.fecha.year ) ][ 'value' ] += vta.monto
            if fecha < vta.fecha:
                fecha = vta.fecha
        if datetime.date( 2000, 1, 1 ) == fecha:
            fecha = "Sin Ventas"        
        totales[ 'ventas' ] += ventas
        data.append( {
            'idcte'     : cte.pk,
            'idusrcte'  : cte.idusuario,
            'cte'       : "{}".format( cte ),
            'idvend'    : cte.compra_a.pk,
            'vend'      : "{}".format( cte.compra_a ),
            'ventas'    : ventas,
            'fecha'     : fecha
        } )
    return render(
        request,
        'productos/reportes/ventas.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Reporte de Ventas',
            'data' : data,
            'show_vendedor' : show_vendedor,
            'fecha_inicio' : fecha_inicio,
            'fecha_fin' : fecha_fin,
            'req_ui' : requires_jquery_ui( request ),
            'totales' : totales,
            'encargados' : get_encardados( usuario ),
            'actual' : actual,
            'req_chart' : True,
            'graph_regs' : procesa_graph_regs( graph_regs )
        } )

@valida_acceso( [ 'abono.pagos_abono' ] )
def pagos( request ):
    show_vendedor = False
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if usuario.is_superuser \
            or usuario.groups.filter( name__icontains = "Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Super-Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Gerente" ).exists():
        show_vendedor = True
    actual = 0
    data = []
    totales = { 'pagos' : Decimal( 0.0 ) }
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
    graph_regs = {}
    for y in range( \
            int( "{:04d}{:02d}".format( fecha_inicio.year, fecha_inicio.month ) ), \
            int( "{:04d}{:02d}".format( fecha_fin.year, fecha_fin.month ) ) + 1 ):
        if 1 <= y % 100 and y % 100 <= 12:
            graph_regs[ "{}-{:04.0f}".format( month_name( y % 100 ), y / 100 ) ] = { 
                'key' : "{}-{:04.0f}".format( month_name( y % 100 ), y / 100 ), 
                'value' : Decimal( 0.0 ) 
                }
    for cte in ctes:
        fecha = datetime.date( 2000, 1, 1 )
        pagos = Decimal( 0.0 )
        for vta in Cargo.objects.filter( cliente = cte ):
            for pago in Abono.objects.filter( cargo = vta, fecha__gte = fecha_inicio, fecha__lte = fecha_fin ):
                pagos += pago.monto
                graph_regs[ "{}-{:04d}".format( month_name( pago.fecha.month ), pago.fecha.year ) ][ 'value' ] += pago.monto
                if fecha < pago.fecha:
                    fecha = pago.fecha
        if datetime.date( 2000, 1, 1 ) == fecha:
            fecha = "Sin Pagos en el Periodo Seleccionado"
        totales[ 'pagos' ] += pagos
        data.append( {
            'idcte'     : cte.pk,
            'idusrcte'  : cte.idusuario,
            'cte'       : "{}".format( cte ),
            'idvend'    : cte.compra_a.pk,
            'vend'      : "{}".format( cte.compra_a ),
            'pagos'     : pagos,
            'fecha'     : fecha
        } )
    return render(
        request,
        'productos/reportes/pagos.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Reporte de Pagos',
            'data' : data,
            'show_vendedor' : show_vendedor,
            'fecha_inicio' : fecha_inicio,
            'fecha_fin' : fecha_fin,
            'req_ui' : requires_jquery_ui( request ),
            'totales' : totales,
            'encargados' : get_encardados( usuario ),
            'actual' : actual,
            'req_chart' : True,
            'graph_regs' : procesa_graph_regs( graph_regs )
        } )

@valida_acceso( [ 'hojaliquidacion.genhojaliquidacion_hoja liquidacion' ] )
def genHojasLiquidacion( request ):
    mensaje = None
    show_vendedor = False
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if usuario.is_superuser \
            or usuario.groups.filter( name__icontains = "Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Super-Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Gerente" ).exists():
        show_vendedor = True
    actual = 0
    today = datetime.date.today()
    prevmonth = today - datetime.timedelta( days = 30 )
    fecha_inicio = datetime.date( prevmonth.year, prevmonth.month, 1 )
    if 2 == today.month:
        fecha_fin = datetime.date( today.year, today.month, 28 )
    elif today.month in [ 4, 6, 9, 11 ]:
        fecha_fin = datetime.date( today.year, today.month, 30 )
    else:
        fecha_fin = datetime.date( today.year, today.month, 31 )
    if "POST" == request.method:
        if "filter" == request.POST.get( "action" ):
            fecha_inicio = datetime.datetime.strptime( request.POST.get( 'fecha_inicio' ), '%Y-%m-%d' )
            fecha_fin = datetime.datetime.strptime( request.POST.get( 'fecha_fin' ), '%Y-%m-%d' )
            if "" != request.POST.get( 'idusrvendedor' ):
                actual = int( "0" + request.POST.get( 'idusrvendedor' ) )
                usr = Usr.objects.get( pk = actual )
                ctes = Vendedor.get_from_usr( usr ).clientes()
            else:
                ctes = get_ctes_from_usr( usuario )
        elif "create_hl" == request.POST.get( "action" ):
            pagos = request.POST.getlist( "idpago" )
            identificador = request.POST.get( "identificador" )
            fecha_entrega = request.POST.get( "fecha_entrega" )
            hl = HojaLiquidacion.objects.create( 
                identificador = identificador,
                fecha_entrega = fecha_entrega,
                generada_por = usuario
                )
            for p in pagos:
                pago = Abono.objects.get( pk = p )
                pago.hoja_de_liquidacion = hl
                pago.actualizable = False
                pago.save()
            if usuario.has_perm_or_has_perm_child( 'hojaliquidacion.ver_detalle_de_hojas_de_liquidacion_hoja liquidacion' ):
                return HttpResponseRedirect( reverse( 'reporte_productos_det_hojliq', kwargs = { 'pk' : hl.pk } ) )
            else:
                mensaje = "Se ha generado la Hoja de Liquidacion: {}".format( hl.identificador )
    else:
        ctes = get_ctes_from_usr( usuario )
    data = []
    for cte in ctes:
        for vta in Cargo.objects.filter( cliente = cte ):
            for pago in Abono.objects.filter( cargo = vta, fecha__gte = fecha_inicio, fecha__lte = fecha_fin, hoja_de_liquidacion = None ):
                data.append( {
                    'idcte'     : cte.pk,
                    'idusrcte'  : cte.idusuario,
                    'cte'       : "{}".format( cte ),
                    'idvend'    : cte.compra_a.pk,
                    'vend'      : "{}".format( cte.compra_a ),
                    'idpago'    : pago.pk,
                    'no'        : pago.no_de_pago,
                    'concepto'  : pago.concepto,
                    'fecha'     : pago.fecha,
                    'monto'     : pago.monto
                } )
    return render( 
        request, 
        'productos/hojasliquidacion/generacion.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Hojas de Liquidación',
            'titulo_descripcion' : 'Generación',
            'req_ui' : requires_jquery_ui( request ),
            'encargados' : get_encardados( usuario ),
            'actual' : actual,
            'show_vendedor' : show_vendedor,
            'fecha_inicio' : fecha_inicio,
            'fecha_fin' : fecha_fin,
            'data' : data,
            'today' : today.strftime( '%Y-%m-%d' ),
            'mensaje' : mensaje
        } )

@valida_acceso( [ 'hojaliquidacion.hojaliquidacion_hoja liquidacion' ] )
def hojasLiquidacion( request ):
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    data = HojaLiquidacion.objects.all().order_by( '-fecha_banco', '-fecha_entrega', 'identificador' )
    can_see_det = usuario.has_perm_or_has_perm_child( 'hojaliquidacion.ver_detalle_de_hojas_de_liquidacion_hoja liquidacion' )
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'hojaliquidacion.genhojaliquidacion_hoja liquidacion' ):
        toolbar.append( { 'type' : 'link', 'view' : 'reporte_productos_gen_hojliq', 'label' : '<i class="far fa-file"></i> Generar' } )
    data2 = []
    for d in data:
        total = Decimal( 0.0 )
        for p in Abono.objects.filter( hoja_de_liquidacion = d ):
            total += p.monto
        data2.append( {
            'id': d.pk,
            'identificador': d.identificador,
            'fecha_creacion': d.fecha_creacion,
            'fecha_entrega': d.fecha_entrega,
            'fecha_banco' : d.fecha_banco,
            'generada_por': d.generada_por,
            'total' : total
        } )
    return render( 
        request, 
        'productos/hojasliquidacion/index.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Hojas de Liquidación',
            'data' : data2,
            'can_see_det' : can_see_det,
            'toolbar' : toolbar
        } )

@valida_acceso( [ 'hojaliquidacion.ver_detalle_de_hojas_de_liquidacion_hoja liquidacion' ] )
def detalleHojaLiquidación( request, pk ):
    if not HojaLiquidacion.objects.filter( pk = pk ).exists():
        return HttpResponseRedirect( reverse( 'seguridad_item_no_encontrado' ) )
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    obj = HojaLiquidacion.objects.get( pk = pk )
    if "POST" == request.method:
        if "" != request.POST.get( 'fecha_banco' ):
            obj.fecha_banco = request.POST.get( 'fecha_banco' )
        if "" != request.POST.get( 'banco' ):
            obj.banco = request.POST.get( 'banco' )
        if "" != request.POST.get( 'referencia' ):
            obj.referencia = request.POST.get( 'referencia' )
        if "" != request.POST.get( 'no_autorizacion' ):
            obj.no_autorizacion = request.POST.get( 'no_autorizacion' )
        obj.save()
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'hojaliquidacion.hojaliquidacion_hoja liquidacion' ):
        toolbar.append( { 'type' : 'link', 'view' : 'reporte_productos_hojliq', 'label' : '<i class="fas fa-list-ul"></i> Ver Todas' } )
    pagos = Abono.objects.filter( hoja_de_liquidacion = obj )
    can_edit = usuario.has_perm_or_has_perm_child( 'hojaliquidacion.agregar_fecha_de_deposito_bancario_hoja liquidacion' )
    can_edit = ( can_edit and ( obj.fecha_banco is None or obj.banco is None or obj.referencia is None or obj.no_autorizacion is None ) )
    suma = Decimal( 0.0 )
    for p in pagos:
        suma += p.monto
    return render( 
        request, 
        'productos/hojasliquidacion/detalle.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Hoja de Liquidación',
            'titulo_descripcion' : obj.identificador,
            'hl' : obj,
            'pagos' : pagos,
            'can_edit' : can_edit,
            'req_ui' : requires_jquery_ui( request ),
            'total' : suma,
            'toolbar' : toolbar
        } )

def get_encardados( usr ):
    usuario = usr
    if usuario.is_superuser \
            or usuario.groups.filter( name__icontains = "Administrador" ).exists() \
            or usuario.groups.filter( name__icontains = "Super-Administrador" ).exists():
        show_vendedor = True
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

