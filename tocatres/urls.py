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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from seguridad import views
from seguridad import vw_permiso, vw_perfil, vw_usuario
from autenticacion import vw_perms, vw_users
from buyersandsellers import vw_cliente, vw_vendedor, vw_gerente, vw_indicadores_vendedor
from productos import vw_producto, vw_campania, vw_cargos_abonos, vw_productos_reportes

urlpatterns = [
    path( 'admin/', admin.site.urls ),

    path( 'elemento-no-encontrado/',    views.item_not_found,       name = 'seguridad_item_no_encontrado' ),
    path( 'elemento-con-relaciones/',   views.item_with_relations,  name = 'seguridad_item_con_relaciones' ),
    path( 'logout/',                    views.logout,               name = 'seguridad_logout' ),
    path( 'my-dashboard/',              views.index,                name = 'seguridad_inicio' ),
    path( '',                           views.login,                name = 'seguridad_login' ),

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

    path( 'indicadores/',   vw_indicadores_vendedor.index, name = "indicadores_inicio" ),

    path( 'gerentes/actualizar/<pk>/',  vw_gerente.update,  name = 'gerente_actualizar' ),
    path( 'gerentes/eliminar/<pk>/',    vw_gerente.delete,  name = 'gerente_eliminar' ),
    path( 'gerentes/nuevo/',            vw_gerente.new,     name = 'gerente_nuevo' ),
    path( 'gerentes/<pk>/',             vw_gerente.see,     name = 'gerente_ver' ),
    path( 'gerentes/',                  vw_gerente.index,   name = 'gerente_inicio' ),

    path( 'vendedores/actualizar/<pk>/',    vw_vendedor.update, name = 'vendedor_actualizar' ),
    path( 'vendedores/eliminar/<pk>/',      vw_vendedor.delete, name = 'vendedor_eliminar' ),
    path( 'vendedores/nuevo/',              vw_vendedor.new,    name = 'vendedor_nuevo' ),
    path( 'vendedores/<pk>/',               vw_vendedor.see,    name = 'vendedor_ver' ),
    path( 'vendedores/',                    vw_vendedor.index,  name = 'vendedor_inicio' ),

    path( 'clientes/actualizar/<pk>/',  vw_cliente.update,      name = 'cliente_actualizar' ),
    path( 'clientes/eliminar/<pk>/',    vw_cliente.delete,      name = 'cliente_eliminar' ),
    path( 'clientes/notas/<pk>/',       vw_cliente.get_notas,   name = 'cliente_get_notas' ),
    path( 'clientes/nuevo/',            vw_cliente.new,         name = 'cliente_nuevo' ),
    path( 'clientes/<pk>/',             vw_cliente.see,         name = 'cliente_ver' ),
    path( 'clientes/',                  vw_cliente.index,       name = 'cliente_inicio' ),

    path( 'productos/actualizar/<pk>/', vw_producto.update, name = 'producto_actualizar' ),
    path( 'productos/eliminar/<pk>/',   vw_producto.delete, name = 'producto_eliminar' ),
    path( 'productos/nuevo/',           vw_producto.new,    name = 'producto_nuevo' ),
    path( 'productos/<pk>/',            vw_producto.see,    name = 'producto_ver' ),
    path( 'productos/',                 vw_producto.index,  name = 'producto_inicio' ),

    path( 'campanias/asignar/',         vw_campania.assign,     name = 'campaña_asignar' ),
    path( 'campanias/actualizar/<pk>/', vw_campania.update,     name = 'campaña_actualizar' ),
    path( 'campanias/eliminar/<pk>/',   vw_campania.delete,     name = 'campaña_eliminar' ),
    path( 'campanias/nuevo/',           vw_campania.new,        name = 'campaña_nuevo' ),
    path( 'campanias/<pk>/',            vw_campania.see,        name = 'campaña_ver' ),
    path( 'campanias/',                 vw_campania.index,      name = 'campaña_inicio' ),

    path( 'novedades/<pk>/<mp>/',       vw_producto.detalle,    name = "campaña_novedades_producto" ),
    path( 'novedades/',                 vw_campania.novedades,  name = 'campaña_novedades' ),

    path( 'movimientos/<pk>/',          vw_cargos_abonos.account,   name = 'cargos_abonos_edocta' ),
    path( 'movimientos/',               vw_cargos_abonos.index,     name = 'cargos_abonos_inicio' ),
    path( 'movimientos/ventas/<pk>/',   vw_cargos_abonos.getcargos, name = 'cargos_abonos_get_cargos' ),

    path( 'ventas/eliminar/<pk>/<pkcte>/',  vw_cargos_abonos.delete_cargo,  name = 'cargos_abonos_eliminar_cargo' ),
    path( 'pagos/eliminar/<pk>/<pkcte>/',   vw_cargos_abonos.delete_abono,  name = 'cargos_abonos_eliminar_abono' ),

    path( 'tu-saldo/', vw_cargos_abonos.mi_saldo,   name = 'mi_saldo' ),

    path( 'saldos/',                                        vw_productos_reportes.saldos,                   name = 'reporte_productos_saldos' ),
    path( 'reportes/ventas/',                               vw_productos_reportes.ventas,                   name = 'reporte_productos_ventas' ),
    path( 'reportes/pagos/',                                vw_productos_reportes.pagos,                    name = 'reporte_productos_pagos' ),
    path( 'reportes/generar-hoja-de-liquidacion/',          vw_productos_reportes.genHojasLiquidacion,      name = 'reporte_productos_gen_hojliq' ),
    path( 'reportes/hojas-de-liquidacion/',                 vw_productos_reportes.hojasLiquidacion,         name = 'reporte_productos_hojliq' ),
    path( 'reportes/detalle-de-hoja-de-liquidacion/<pk>/',  vw_productos_reportes.detalleHojaLiquidación,   name = 'reporte_productos_det_hojliq' ),    
]

urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
urlpatterns += staticfiles_urlpatterns()