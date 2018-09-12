from django.db import models
from datetime import date
from decimal import Decimal

from buyersandsellers.models import *
from seguridad.models import *

# Create your models here.

class Producto( models.Model ):
    idproducto = models.AutoField( primary_key = True )
    nombre = models.CharField( blank = False, max_length = 100 )
    sku = models.CharField( blank = False, max_length = 25 )
    imagen = models.ImageField( blank = True, null = True, upload_to = 'productos' )
    esta_activo = models.BooleanField( default = True )
    marca = models.CharField( max_length = 100, null = True )
    modelo = models.CharField( max_length = 100, null = True )
    categoria = models.CharField( blank = True, null = True, max_length = 100 )
    precio_de_compra = models.DecimalField( max_digits = 9, decimal_places = 2, default = 0.0 )
    precio_de_venta = models.DecimalField( max_digits = 9, decimal_places = 2, default = 0.0 )
    descripcion = models.TextField()
    class Meta:
        ordering = [ '-esta_activo', 'sku', 'categoria', 'marca', 'modelo', 'nombre' ]
    def __unicode__( self ):
        name = ""
        if self.nombre:
            name = self.nombre
        if self.marca:
            if "" != name:
                name += " " + self.marca
            else:
                name += self.marca
        if self.modelo:
            if "" != name:
                name += " " + self.modelo
            else:
                name += self.modelo
        return name
    def __str__( self ):
        return self.__unicode__()

class Campaña( models.Model ):
    idcampaña = models.AutoField( primary_key = True )
    nombre = models.CharField( blank = False, max_length = 100 )
    fecha_de_inicio = models.DateField( default = date.today )
    fecha_de_termino = models.DateField( default = date.today )
    mostrar_precio_de_venta = models.BooleanField( default = False )
    productos = models.ManyToManyField( Producto, related_name = '+', limit_choices_to = { 'esta_activo' : True } )
    usuarios = models.ManyToManyField( Usr, related_name = '+', limit_choices_to = { 'is_active' : True } )
    class Meta:
        ordering = [ 'nombre', '-fecha_de_inicio', '-fecha_de_termino' ]
    def __unicode__( self ):
        return "{} ({} a {})".format( self.nombre, self.fecha_de_inicio.strftime( '%d/%m/%Y' ), self.fecha_de_termino.strftime( '%d/%m/%Y' ) )
    def __str__( self ):
        return self.__unicode__()

class Cargo( models.Model ):
    idcargo = models.AutoField( primary_key = True )
    fecha = models.DateField( default = date.today )
    factura = models.CharField( blank = False, max_length = 20 )
    producto = models.ForeignKey( Producto, related_name = '+', on_delete = models.SET_NULL, null = True, limit_choices_to =  { 'esta_activo' : True } )
    concepto = models.CharField( blank = False, max_length = 150 )
    monto = models.DecimalField( max_digits = 9, decimal_places = 2, default = 0.0 )
    cliente = models.ForeignKey( Usr, related_name = '+', on_delete = models.PROTECT, limit_choices_to = { 'is_active' : True } )
    vendedor = models.ForeignKey( Usr, related_name = '+', on_delete = models.SET_NULL, null = True, limit_choices_to = { 'is_active' : True } )
    actualizable = models.BooleanField( default = True )
    saldado = models.BooleanField( default = False )
    class Meta:
        ordering = [ 'cliente', 'fecha', 'factura' ]
    def __unicode__( self ):
        return "{}. {}".format( self.factura, self.concepto )
    def __str__( self ):
        return self.__unicode__()
    def saldo( self ):
        saldo = self.monto
        abonos = Abono.objects.filter( cargo = self )
        for abono in abonos:
            saldo -= abono.monto
        return saldo
    def no_abonos( self ):
        return len( Abono.objects.filter( cargo = self ) )

class HojaLiquidacion( models.Model ):
    idhojaliquidacion = models.AutoField( primary_key = True )
    identificador = models.CharField( blank = False, max_length = 100 )
    fecha_creacion = models.DateField( default = date.today )
    fecha_entrega = models.DateField( default = date.today )
    fecha_banco = models.DateField( blank = True, null = True )
    generada_por = models.ForeignKey( Usr, related_name = '+', on_delete = models.PROTECT )
    banco = models.CharField( blank = True, null = True, max_length = 100 )
    referencia = models.CharField( blank = True, null = True, max_length = 100 )
    no_autorizacion = models.CharField( blank = True, null = True, max_length = 100 )
    class Meta:
        ordering = [ 'fecha_creacion', 'fecha_entrega', 'fecha_banco', 'identificador' ]
    def __unicode__( self ):
        return "{}".format( self.identificador )
    def __str__( self ):
        return self.__unicode__

class Abono( models.Model ):
    idabono = models.AutoField( primary_key = True )
    fecha = models.DateField( default = date.today )
    no_de_pago = models.PositiveSmallIntegerField( default = 1, blank = False )
    cargo = models.ForeignKey( Cargo, related_name = '+', on_delete = models.CASCADE, limit_choices_to = { 'saldado' : False } )
    concepto = models.CharField( blank = False, max_length = 150 )
    monto = models.DecimalField( max_digits = 9, decimal_places = 2, default = 0.0 )
    vendedor = models.ForeignKey( Usr, related_name = '+', on_delete = models.SET_NULL, null = True, limit_choices_to = { 'is_active' : True } )
    actualizable = models.BooleanField( default = True )
    hoja_de_liquidacion =  models.ForeignKey( HojaLiquidacion, related_name = '+', on_delete = models.SET_NULL, blank = True, null = True, default = None )
    class Meta:
        ordering = [ 'fecha', 'no_de_pago' ]
    def __unicode__( self ):
        return "{:03d}. {} ({})".format( self.no_de_pago, self.concepto, self.cargo.factura )
    def __str__( self ):
        return self.__unicode__()

def movimientos( cliente ):
    res = {
        'ventas' : Decimal( 0.0 ),
        'pagos' : Decimal( 0.0 ),
        'saldo' : Decimal( 0.0 ),
        'ultimo_pago' : date( 2000, 1, 1 ),
        'rec_vta' : Decimal( 0.0 ),
        'rec_pag' : Decimal( 0.0 )
    }
    for vta in Cargo.objects.filter( cliente = cliente ):
        res[ 'ventas' ] += vta.monto
        res[ 'saldo' ] += vta.saldo()
        for pago in Abono.objects.filter( cargo = vta, fecha__gte = res[ 'ultimo_pago' ] ):
            if res[ 'ultimo_pago' ] < pago.fecha:
                res[ 'ultimo_pago' ] = pago.fecha
        if vta.saldo() > 0:
            res[ 'rec_vta' ] += vta.monto
            res[ 'rec_pag' ] += ( vta.monto - vta.saldo() )
    if date( 2000, 1, 1 ) == res[ 'ultimo_pago' ]:
        res[ 'ultimo_pago' ] = "Sin Pagos"
    res[ 'pagos' ] = res[ 'ventas' ] - res[ 'saldo' ]
    return res
