from django.db import models
from seguridad.models import Usr
from tocatres.utils import *

# Create your models here.

class Vendedor( Usr ):
    idvendedor = models.AutoField( primary_key = True )
    reporta_a = models.ForeignKey( 'self', on_delete = models.CASCADE, related_name = '+', blank = True, null = True )
    def __unicode__( self ):
        return "{}".format( self.first_name )
    def __str__( self ):
        return self.__unicode__()
    def clientes( self ):
        return Cliente.objects.filter( depende_de__pk = self.idusuario ).order_by( 'first_name', 'last_name' )
    def all_clientes( self ):
        ctes = list( self.clientes() )
        for vend in Vendedor.get_Vendedores( self ):
            for cte in vend.clientes():
                ctes.append( cte )
        return ctes
    def get_from_usr( usr ):
        if Vendedor.objects.filter( idusuario = usr.pk ).exists():
            return Vendedor.objects.get( idusuario = usr.pk )
        return None
    def get_Gerentes():
        """
        Devuelve QuerySet de vendedores que son gerentes (que no dependen de nadie)
        """
        return Vendedor.objects.filter( reporta_a = None ).order_by( 'first_name', 'last_name' )
    def get_Vendedores( gerente = None ):
        """
        gerente debe ser de tipo vendedores

        Devuelve la lista de vendedores
        """
        vendedores = []
        if gerente is None:
            gerentes = Vendedor.get_Gerentes()
        else:
            gerentes = [ gerente ]
        for gerente in gerentes:
            for v in Vendedor.objects.filter( reporta_a = gerente ).order_by( 'first_name', 'last_name' ):
                vendedores.append( v )
        return vendedores

class Cliente( Usr ):
    idcliente = models.AutoField( primary_key = True )
    compra_a = models.ForeignKey( Vendedor, on_delete = models.CASCADE, related_name = '+' )
    alias = models.CharField( blank = False, max_length = 100 )
    texto_productos = models.CharField( blank = True, max_length = 250, default = 'Productos que pueden interesarte...' )
    clave = models.CharField( blank = False, max_length = 15, default = "0000" )
    def __unicode__( self ):
        return "{}".format( self.get_full_name() )
    def __str__( self ):
        return self.__unicode__()
    def get_from_usr( usr ):
        if Cliente.objects.filter( idusuario = usr.pk ).exists():
            return Cliente.objects.get( idusuario = usr.pk )
        return None
