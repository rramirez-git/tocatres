from django.db import models
from seguridad.models import Usr
from tocatres.utils import *

# Create your models here.

class Vendedor( Usr ):
    idvendedor = models.AutoField( primary_key = True )
    reporta_a = models.ForeignKey( 'self', on_delete = models.CASCADE, related_name = '+', blank = True, null = True )
    def __unicode__( self ):
        return "{} ({})".format( self.get_full_name(), self.usuario )
    def __str__( self ):
        return "{} ({})".format( self.get_full_name(), self.usuario )
    def clientes( self ):
        return Cliente.objects.filter( depende_de__pk = self.idusuario )
    def all_clientes( self ):
        ctes = []
        for cte in self.clientes():
            ctes.append( cte )
        for vend in self.descendencia():
            if vend.groups.filter( name = 'Vendedor' ).exists():
                for cte in Cliente.objects.filter( depende_de = vend ):
                    ctes.append( cte )
        return ctes

class Cliente( Usr ):
    idcliente = models.AutoField( primary_key = True )
    compra_a = models.ForeignKey( Vendedor, on_delete = models.CASCADE, related_name = '+' )
    def __unicode__( self ):
        return "{} ({})".format( self.get_full_name(), self.usuario )
    def __str__( self ):
        return "{} ({})".format( self.get_full_name(), self.usuario )