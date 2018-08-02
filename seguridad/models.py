from django.db import models
from django.contrib.auth.models import Permission, User

from tocatres.utils import *

# Create your models here.

class Permiso( Permission ):
    idpermiso = models.AutoField( primary_key = True )
    nombre = models.CharField( blank = False, max_length = 100 )
    descripcion = models.TextField()
    vista = models.CharField( max_length = 100, null = True )
    permiso_padre = models.ForeignKey( 'self', on_delete = models.CASCADE, related_name = '+', blank = True, null = True )
    es_operacion = models.BooleanField( default = False )
    posicion = models.PositiveSmallIntegerField( default = 0 )
    def __unicode__( self ):
        return self.nombre
    def __str__( self ):
        return self.nombre
    def hijos( self ):
        objs = Permiso.objects.filter( permiso_padre__pk = self.pk ).order_by( 'posicion' )
        return objs
    def descendencia( self ):
        desc = []
        for hijo in self.hijos():
            desc.append( hijo )
            for nieto in hijo.descendencia():
                desc.append( nieto )
        return desc
    def depth( self ):
        if self.permiso_padre is None:
            return 0
        else:
            return self.permiso_padre.depth() + 1
    def depth_name( self, fill_with = '&nbsp;&nbsp;&nbsp;&nbsp;' ):
        return "{}{}".format( fill_with * self.depth(), self )
    def perm( self ):
        return super( Permiso, self )
    def get_from_perms( model, codename ):
        """
        Obtiene un Permiso con base en el permission
        """
        perm = Permission.objects.filter( content_type__model = model, codename = codename )
        if 0 == perm.count():
            return None
        permiso = Permiso.objects.filter( id = perm[ 0 ].pk )
        if 0 == permiso.count():
            return None
        return permiso[ 0 ]
    def get_from_package_codename( model_codename ):
        """
        Obtiene un Permiso con base en el permission en formato "model.codename"
        """
        elems = model_codename.split( '.' )
        return Permiso.get_from_perms( elems[ 0 ], elems[ 1 ] )

class Usr( User ):
    idusuario = models.AutoField( primary_key = True )
    usuario = models.CharField( blank = False, unique = True, max_length = 50 )
    contraseña = models.CharField( blank = False, max_length = 250 )
    telefono = models.CharField( max_length = 15, blank = True, null = True )
    celular = models.CharField( max_length = 15, blank = True, null = True )
    fotografia = models.ImageField( blank = True, null = True, upload_to = 'usuarios' )
    depende_de = models.ForeignKey( 'self', on_delete = models.CASCADE, related_name = '+', blank = True, null = True )
    def __unicode__( self ):
        return self.get_full_name()
    def __str__( self ):
        return self.get_full_name()
    def hijos( self ):
        return Usr.objects.filter( depende_de__pk = self.pk )
    def depth( self ):
        if self.depende_de is None:
            return 0
        return self.depende_de.depth() + 1
    def depth_name( self, fill_with = '&nbsp;&nbsp;&nbsp;&nbsp;' ):
        return "{}{}".format( fill_with * self.depth(), self )
    def descendencia( self ):
        desc = []
        for hijo in self.hijos():
            desc.append( hijo )
            for nieto in hijo.descendencia():
                desc.append( nieto )
        return desc
    def has_perm_or_has_perm_child( self, model_codename ):
        perms = []
        permiso = Permiso.get_from_package_codename( model_codename )
        if permiso is None:
            print_error( "No se encontró el permiso: " + model_codename )
            return False
        perms.append( permiso.perm() )
        desc = permiso.descendencia()
        for p in desc:
            perms.append( p.perm() )
        for perm in perms:
            p = "{}.{}".format( perm.content_type.app_label, perm.codename )
            if super( Usr, self ).has_perm( p ):
                return True
        return False
    def main_menu_struct( self ):
        mm = []
        root_perms = Permiso.objects.filter( permiso_padre__isnull = True ).order_by( 'posicion' )
        for rp in root_perms:
            if self.has_perm_or_has_perm_child( "{}.{}".format( rp.content_type.model, rp.codename ) ):
                items = []
                for p in rp.descendencia():
                    if False == p.es_operacion and self.has_perm_or_has_perm_child( "{}.{}".format( p.content_type.model, p.codename ) ):
                        items.append( p )
                item = { 'permiso' : rp, 'items' : items, 'items_qty' : len(items) }
                mm.append( item )
        return mm



