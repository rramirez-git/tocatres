from django.db.models import Sum
from productos.models import Cargo, Abono

def upd_venta_pago():
    vtas = list(Cargo.objects.filter( iva = 0, subtotal = 0 ))
    cvtas = len(vtas)
    cpagos = 0
    for vta in vtas:
        vta.porcentaje_de_iva = vta.producto.porcentaje_de_iva
        vta.subtotal = vta.monto / ( ( 100 + vta.porcentaje_de_iva ) / 100 )
        vta.iva = vta.monto - vta.subtotal
        vta.save()
        pagos = list( Abono.objects.filter( cargo = vta, iva = 0, subtotal = 0 ) )
        cpagos += len(pagos)
        for pago in pagos:
            pago.subtotal = pago.monto / ( ( 100 + vta.porcentaje_de_iva ) / 100 )
            pago.iva = pago.monto - pago.subtotal
            pago.save()
    print("{:04d} pagos actualizados en {:04d} ventas actualizadas".format(cpagos,cvtas))
    return {'cpagos':cpagos, 'cvtas':cvtas}

def verify_saldos():
    vtas_subtotal = Cargo.objects.all().aggregate( Sum( 'subtotal' ) )[ 'subtotal__sum' ]
    vtas_iva = Cargo.objects.all().aggregate( Sum( 'iva' ) )[ 'iva__sum' ]
    vtas_total = Cargo.objects.all().aggregate( Sum( 'monto' ) )[ 'monto__sum' ]
    pagos_subtotal = Abono.objects.all().aggregate( Sum( 'subtotal' ) )[ 'subtotal__sum' ]
    pagos_iva = Abono.objects.all().aggregate( Sum( 'iva' ) )[ 'iva__sum' ]
    pagos_total = Abono.objects.all().aggregate( Sum( 'monto' ) )[ 'monto__sum' ]
    print( '\nResumen de Ventas:\n' )
    print( " +-{}-+-{}-+-{}-+-{}-+".format( "-" * 10, "-" * 13, "-" * 13, "-" * 13 ) )
    print( " | {:10} | {:13} | {:13} | {:13} |".format( 'Dato', "Subtotal", "IVA", "Total" ) )
    print( " +-{}-+-{}-+-{}-+-{}-+".format( "-" * 10, "-" * 13, "-" * 13, "-" * 13 ) )
    print( " | {:10} | {:13.2f} | {:13.2f} | {:13.2f} |".format( 'Ventas', vtas_subtotal, vtas_iva, vtas_total ) )
    print( " | {:10} | {:13.2f} | {:13.2f} | {:13.2f} |".format( 'Pagos', pagos_subtotal, pagos_iva, pagos_total ) )
    print( " +-{}-+-{}-+-{}-+-{}-+\n".format( "-" * 10, "-" * 13, "-" * 13, "-" * 13 ) )
    vtas =[ vta for vta in Cargo.objects.all() if vta.saldo() < 0 ]
    if len( vtas ):
        print( '\nVentas con Saldos Negativos:\n' )
        print( " +-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+".format( "-" * 50, "-" * 10, "-" * 10, "-" * 50, "-" * 50, "-" * 13, "-" * 13 ) )
        print( " | {:50} | {:10} | {:10} | {:50} | {:50} | {:13} | {:13} |".format( "Cliente", "Fecha", "Factura", "Producto", "Concepto", "Monto", "Saldo" ) )
        print( " +-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+".format( "-" * 50, "-" * 10, "-" * 10, "-" * 50, "-" * 50, "-" * 13, "-" * 13 ) )
        for vta in vtas:
            print( " | {:50} | {:%d-%m-%Y} | {:10} | {:50} | {:50} | {:13.2f} | {:13.2f} |".format( "{}".format( vta.cliente ), vta.fecha, vta.factura, "{}".format( vta.producto ), vta.concepto, vta.monto, vta.saldo() ) )
        print( " +-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+-{}-+".format( "-" * 50, "-" * 10, "-" * 10, "-" * 50, "-" * 50, "-" * 13, "-" * 13 ) )
        print( '' )
    else:
        print( '\nSin Ventas con Saldos Negativos:\n' )
