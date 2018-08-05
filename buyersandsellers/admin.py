from django.contrib import admin
from .models import *

# Register your models here.

class AdminVendedor( admin.ModelAdmin ):
    list_display = [ 'fotografia', 'usuario', 'first_name', 'last_name' ]
    list_display_links = [ 'usuario' ]
    search_fields = [ 'usuario', 'first_name', 'last_name' ]
    list_editable = [ 'first_name', 'last_name' ]
    class Meta:
        model = Vendedor

class AdminCliente( admin.ModelAdmin ):
    list_display = [ 'fotografia', 'usuario', 'first_name', 'last_name' ]
    list_display_links = [ 'usuario' ]
    search_fields = [ 'usuario', 'first_name', 'last_name' ]
    list_editable = [ 'first_name', 'last_name' ]
    class Meta:
        model = Cliente

admin.site.register( Vendedor, AdminVendedor )
admin.site.register( Cliente, AdminCliente )