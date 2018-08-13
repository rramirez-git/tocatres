"""tocatres URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from seguridad import views
from seguridad import vw_permiso, vw_perfil, vw_usuario
from autenticacion import vw_perms, vw_users
from buyersandsellers import vw_cliente, vw_vendedor

urlpatterns = [
    path( 'admin/', admin.site.urls ),

    path( 'logout/',        views.logout,   name = 'seguridad_logout' ),
    path( 'my-dashboard/',  views.index,    name = 'seguridad_inicio' ),
    path( '',               views.login,    name = 'seguridad_login' ),

    path( 'permisos/actualizar/<pk>/',  vw_permiso.update,  name = "permiso_actualizar" ),
    path( 'permisos/eliminar/<pk>/',    vw_permiso.delete,  name = "permiso_eliminar" ),
    path( 'permisos/nuevo/',            vw_permiso.new,     name = "permiso_nuevo" ),
    path( 'permisos/<pk>/',             vw_permiso.see,     name = "permiso_ver" ),
    path( 'permisos/',                  vw_permiso.index,   name = 'permiso_inicio' ),
    path( 'perms/',                     vw_perms.index,     name = 'perms_inicio' ),

    path( 'perfiles/actualizar/<pk>/',  vw_perfil.update,   name = 'perfil_actualizar' ),
    path( 'perfiles/eliminar/<pk>/',    vw_perfil.delete,   name = 'perfil_eliminar' ),
    path( 'perfiles/nuevo/',            vw_perfil.new,      name = 'perfil_nuevo' ),
    path( 'perfiles/<pk>/',             vw_perfil.see,      name = 'perfil_ver' ),
    path( 'perfiles/',                  vw_perfil.index,    name = 'perfil_inicio' ),

    path( 'usuarios/actualizar/<pk>/',  vw_usuario.update,  name = "usuario_actualizar" ),
    path( 'usuarios/eliminar/<pk>/',    vw_usuario.delete,  name = "usuario_eliminar" ),
    path( 'usuarios/nuevo/',            vw_usuario.new,     name = "usuario_nuevo" ),
    path( 'usuarios/<pk>/',             vw_usuario.see,     name = "usuario_ver" ),
    path( 'usuarios/',                  vw_usuario.index,   name = "usuario_inicio" ),
    path( 'users/',                     vw_users.index,     name = "users_inicio" ),

    path( 'vendedores/actualizar/<pk>/',    vw_vendedor.update, name = 'vendedor_actualizar' ),
    path( 'vendedores/eliminar/<pk>/',      vw_vendedor.delete, name = 'vendedor_eliminar' ),
    path( 'vendedores/nuevo/',              vw_vendedor.new,    name = 'vendedor_nuevo' ),
    path( 'vendedores/<pk>/',               vw_vendedor.see,    name = 'vendedor_ver' ),
    path( 'vendedores/',                    vw_vendedor.index,  name = 'vendedor_inicio' ),

    path( 'clientes/actualizar/<pk>/',  vw_cliente.update,  name = 'cliente_actualizar' ),
    path( 'clientes/eliminar/<pk>/',    vw_cliente.delete,  name = 'cliente_eliminar' ),
    path( 'clientes/nuevo/',            vw_cliente.new,     name = 'cliente_nuevo' ),
    path( 'clientes/<pk>/',             vw_cliente.see,     name = 'cliente_ver' ),
    path( 'clientes/',                  vw_cliente.index,   name = 'cliente_inicio' ),
    
] + static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
