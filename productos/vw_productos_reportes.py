from django.shortcuts import render

from decimal import Decimal
import datetime

from .models import *

from seguridad.mkitsafe import *
from buyersandsellers.vw_cliente import get_ctes_from_usr
from tocatres.utils import requires_jquery_ui, month_name

@valida_acceso( [ 'abono.saldos_abono' ] )
def saldos( request ):
    mensaje = None
    show_vendedor = False
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if usuario.is_admin():
        show_vendedor = True
    actual = 0
    ctes = get_ctes_from_usr( usuario )
    if "POST" == request.method:
        if "filter_vend" == request.POST.get( 'action' ):
            if "" != request.POST.get( 'idusrvendedor' ):
                actual = int( "0" + request.POST.get( 'idusrvendedor' ) )
                usr = Usr.objects.get( pk = actual )
                ctes = Vendedor.get_from_usr( usr ).clientes()
        elif 'addcharge' == request.POST.get( 'action' ):
            cte = Usr.objects.get( pk = request.POST.get( 'cte' ) )
            prod = Producto.objects.get( pk = request.POST.get( 'product' ) )
            mov = Cargo.objects.create(
                fecha = request.POST.get( 'fecha_cargo' ),
                factura = request.POST.get( 'factura' ),
                concepto = request.POST.get( 'concepto_cargo' ),
                monto = request.POST.get( 'monto_cargo' ),
                producto = prod,
                cliente = cte,
                vendedor = usuario
            )
            mov.porcentaje_de_iva = Decimal( mov.producto.porcentaje_de_iva )
            mov.subtotal = Decimal( mov.monto ) / ( ( 100 + mov.porcentaje_de_iva ) / 100 )
            mov.iva = Decimal( mov.monto ) - mov.subtotal
            mov.save()
            mensaje = { 'type' : 'success', 'msg' : "Se ha agregado la venta de {} a {}".format( prod, cte ) }
        elif 'addpayment' == request.POST.get( 'action' ):
            cte = Usr.objects.get( pk = request.POST.get( 'cte' ) )
            cargo = Cargo.objects.get( pk = request.POST.get( 'cargo' ) )
            mov = Abono.objects.create(
                fecha = request.POST.get( 'fecha_abono' ),
                no_de_pago = request.POST.get( 'no_de_pago' ),
                concepto = request.POST.get( 'concepto_abono' ),
                monto = request.POST.get( 'monto_abono' ),
                cargo = cargo,
                vendedor = usuario
            )
            mov.subtotal = Decimal(  mov.monto ) / ( ( 100 + mov.cargo.porcentaje_de_iva ) / 100 )
            mov.iva = Decimal( mov.monto ) - mov.subtotal
            mov.save()
            mensaje = { 'type' : 'success', 'msg' : "Se ha agregado el pago {} de {} a {}".format( request.POST.get( 'no_de_pago' ), request.POST.get( 'concepto_abono' ), cargo.cliente ) }
            cargo.actualizable = False
            if cargo.saldo() <= 0:
                cargo.saldado = True
            cargo.save()
            if cargo.saldado:
                for abono in Abono.objects.filter( cargo = cargo ):
                    abono.actualizable = False
                    abono.save()
        elif 'add-note' == request.POST.get( 'action' ):
            cte = Cliente.objects.get( pk = request.POST.get( 'idcte' ) )
            NotasCliente.objects.create( cliente = cte, nota = request.POST.get( 'nota' ) )
            actual = int( "0" + request.POST.get( 'idusrvendedor' ) )
            if 0 != actual:
                usr = Usr.objects.get( pk = actual )
                ctes = Vendedor.get_from_usr( usr ).clientes()
            mensaje = { 'type' : 'success', 'msg' : "Se ha agregado la nota a {}".format( cte ) }
    data = []
    totales = { 
        'ventas' : Decimal( 0.0 ), 
        'pagos' : Decimal( 0.0 ), 
        'saldo' : Decimal( 0.0 ), 
        'recuperacion' : Decimal( 0.0 ) 
    }
    rec_vta = Decimal( 0.0 )
    rec_pag = Decimal( 0.0 )
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
            if vta.saldo() > 0:
                rec_vta += vta.monto
                rec_pag += ( vta.monto - vta.saldo() )
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
            'clave'     : "{}".format( cte.clave ),
            'idvend'    : cte.compra_a.pk,
            'vend'      : "{}".format( cte.compra_a ),
            'ventas'    : ventas,
            'pagos'     : pagos,
            'saldo'     : saldo,
            'fecha'     : fecha
        } )
    if rec_vta > 0:
        totales[ 'recuperacion' ] = "{:02.0f}".format( rec_pag * Decimal( 100.0 ) / rec_vta )
    decorado = [ ( tmpusr[ 'saldo' ] <= 0, tmpusr[ 'vend' ], tmpusr[ 'cte' ], i, tmpusr ) for i, tmpusr in enumerate( data ) ]
    decorado.sort()
    data = [ tmpusr for saldo, vend, cte, i, tmpusr in decorado ]
    return render(
        request,
        'productos/reportes/saldos.html', {
            'menu_main' : usuario.main_menu_struct(),
            'footer' : True,
            'titulo' : 'Clientes',
            'data' : data,
            'show_vendedor' : show_vendedor,
            'totales' : totales,
            'encargados' : get_encardados( usuario ),
            'actual' : actual,
            'products' : Producto.objects.all(),
            'req_ui' : requires_jquery_ui( request ),
            'mensaje' : mensaje
        } )

@valida_acceso( [ 'abono.ventas_abono' ] )
def ventas( request ):
    show_vendedor = False
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if usuario.is_admin():
        show_vendedor = True
    actual = 0
    data = []
    totales = { 'ventas' : Decimal( 0.0 ), 'subtotal' : Decimal( 0.0 ), 'iva' : Decimal( 0.0 ) }
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
    for cte in ctes:
        for vta in Cargo.objects.filter( cliente = cte, fecha__gte = fecha_inicio, fecha__lte = fecha_fin ):
            data.append( {
                'idcte'     : cte.pk,
                'idusrcte'  : cte.idusuario,
                'cte'       : "{}".format( cte ),
                'cve'       : cte.clave,
                'idvend'    : cte.compra_a.pk,
                'vend'      : "{}".format( cte.compra_a ),
                'ventas'    : vta.monto,
                'subtotal'  : vta.subtotal,
                'iva'       : vta.iva,
                'fecha'     : vta.fecha,
                'concepto'  : vta.concepto,
                'factura'   : vta.factura
            } )
            totales[ 'ventas' ] += vta.monto
            totales[ 'subtotal' ] += vta.subtotal
            totales[ 'iva' ] += vta.iva
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
            'actual' : actual
        } )

@valida_acceso( [ 'abono.pagos_abono' ] )
def pagos( request ):
    show_vendedor = False
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if usuario.is_admin():
        show_vendedor = True
    actual = 0
    data = []
    totales = { 'pagos' : Decimal( 0.0 ), 'subtotal' : Decimal( 0.0 ), 'iva' : Decimal( 0.0 ) }
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
    for cte in ctes:
        for vta in Cargo.objects.filter( cliente = cte ):
            for pago in Abono.objects.filter( cargo = vta, fecha__gte = fecha_inicio, fecha__lte = fecha_fin ):
                totales[ 'pagos' ] += pago.monto
                totales[ 'subtotal' ] += pago.subtotal
                totales[ 'iva' ] += pago.iva
                data.append( {
                    'idcte'     : cte.pk,
                    'idusrcte'  : cte.idusuario,
                    'cte'       : "{}".format( cte ),
                    'cve'       : cte.clave,
                    'idvend'    : cte.compra_a.pk,
                    'vend'      : "{}".format( cte.compra_a ),
                    'pagos'     : pago.monto,
                    'subtotal'  : pago.subtotal,
                    'iva'       : pago.iva,
                    'fecha'     : pago.fecha,
                    'concepto'  : pago.concepto
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
        } )

@valida_acceso( [ 'hojaliquidacion.genhojaliquidacion_hoja liquidacion' ] )
def genHojasLiquidacion( request ):
    mensaje = None
    show_vendedor = False
    usuario = Usr.objects.filter( id = request.user.pk )[ 0 ]
    if usuario.is_admin():
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
        if "set-data" == request.POST.get( 'action' ):
            if "" != request.POST.get( 'fecha_banco' ):
                obj.fecha_banco = datetime.datetime.strptime( request.POST.get( 'fecha_banco' ), '%Y-%m-%d').date()
            if "" != request.POST.get( 'banco' ):
                obj.banco = request.POST.get( 'banco' )
            if "" != request.POST.get( 'referencia' ):
                obj.referencia = request.POST.get( 'referencia' )
            if "" != request.POST.get( 'no_autorizacion' ):
                obj.no_autorizacion = request.POST.get( 'no_autorizacion' )
        elif "update" == request.POST.get( 'action' ):
            obj.fecha_entrega = datetime.datetime.strptime( request.POST.get( 'fecha_entrega' ), '%Y-%m-%d').date()
            obj.fecha_banco = datetime.datetime.strptime( request.POST.get( 'fecha_banco' ) , '%Y-%m-%d').date()
            obj.banco = request.POST.get( 'banco' )
            obj.referencia = request.POST.get( 'referencia' )
            obj.no_autorizacion = request.POST.get( 'no_autorizacion' )
            for pago in request.POST.getlist( 'removerpago' ):
                p = Abono.objects.get( pk = pago )
                p.hoja_de_liquidacion = None
                p.save()
        obj.save()
    toolbar = []
    if usuario.has_perm_or_has_perm_child( 'hojaliquidacion.hojaliquidacion_hoja liquidacion' ):
        toolbar.append( { 'type' : 'link', 'view' : 'reporte_productos_hojliq', 'label' : '<i class="fas fa-list-ul"></i> Ver Todas' } )
    pagos = Abono.objects.filter( hoja_de_liquidacion = obj )
    can_update = usuario.has_perm_or_has_perm_child( 'hojaliquidacion.actualizar_hoja_de_liquidacion_hoja liquidacion' )
    can_edit = usuario.has_perm_or_has_perm_child( 'hojaliquidacion.agregar_fecha_de_deposito_bancario_hoja liquidacion' )
    can_edit = ( can_edit and ( obj.fecha_banco is None or obj.banco is None or obj.referencia is None or obj.no_autorizacion is None ) )
    if can_update and not can_edit:
        toolbar.append( { 'type' : 'button', 'onclick' : 'HojaLiq.openForUpdate()', 'label' : '<i class="far fa-edit"></i> Actualizar' } )
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
            'can_update' : can_update,
            'req_ui' : requires_jquery_ui( request ),
            'total' : suma,
            'toolbar' : toolbar
        } )

def get_encardados( usr ):
    usuario = usr
    if usuario.is_admin():
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

