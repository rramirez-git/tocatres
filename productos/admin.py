from django.contrib import admin
from .models import *

# Register your models here.

class AdminProducto( admin.ModelAdmin ):
    list_display = [ 'nombre', 'sku', 'esta_activo', 'marca', 'categoria', 'precio_de_compra', 'precio_de_venta' ]
    list_display_links = [ 'nombre' ]
    search_fields = [ 'nombre', 'sku', 'marca', 'categoria' ]
    list_editable = [ 'sku', 'esta_activo', 'marca', 'categoria' ]
    class Meta:
        model = Producto

class AdminCampaña( admin.ModelAdmin ):
    list_display = [ 'nombre', 'fecha_de_inicio', 'fecha_de_termino', 'mostrar_precio_de_venta' ]
    list_display_links = [ 'nombre' ]
    search_fields = [ 'nombre' ]
    list_editable = [ 'fecha_de_inicio', 'fecha_de_termino', 'mostrar_precio_de_venta' ]
    class Meta:
        model = Campaña

class AdminCargo( admin.ModelAdmin ):
    list_display = [ 'fecha', 'factura', 'producto', 'concepto', 'monto', 'cliente' ]
    list_display_links = [ 'factura' ]
    list_editable = [ 'fecha', 'concepto', 'monto' ]
    search_fields = [ 'fecha', 'factura', 'producto', 'concepto', 'cliente' ]
    class Meta:
        model = Abono

class AdminAbono( admin.ModelAdmin ):
    list_display = [ 'fecha', 'no_de_pago', 'cargo', 'concepto', 'monto' ]
    list_display_links = [ 'no_de_pago' ]
    list_editable = [ 'fecha', 'concepto', 'monto' ]
    search_fields = [ 'fecha', 'no_de_pago', 'cargo', 'concepto' ]
    class Meta:
        model = Abono

admin.site.register( Producto, AdminProducto )
admin.site.register( Campaña, AdminCampaña )
admin.site.register( Cargo, AdminCargo )
admin.site.register( Abono, AdminAbono )
