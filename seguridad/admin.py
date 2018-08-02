from django.contrib import admin
from .models import *

# Register your models here.

class AdminPermiso( admin.ModelAdmin ):
    list_display = [ 'permiso', 'permiso_padre', 'descripcion' ]
    list_filter = [ 'permiso_padre' ]
    search_fields = [ 'permiso', 'descripcion', 'permiso_padre' ]
    class Meta:
        model = Permiso

class AdminUsuario( admin.ModelAdmin ):
    list_display = [ 'fotografia', 'usuario', 'first_name', 'last_name' ]
    list_display_links = [ 'usuario' ]
    search_fields = [ 'usuario', 'first_name', 'last_name' ]
    list_editable = [ 'first_name', 'last_name' ]
    class Meta:
        model = Usr

admin.site.register( Permiso, AdminPermiso )
admin.site.register( Usr, AdminUsuario )