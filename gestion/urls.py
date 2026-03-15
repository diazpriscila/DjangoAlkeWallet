from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('clientes/', views.cliente_lista, name='cliente_lista'),
    path('clientes/<int:pk>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/nuevo/', views.cliente_crear, name='cliente_crear'),
    path('clientes/<int:pk>/editar/', views.cliente_editar, name='cliente_editar'),
    path('clientes/<int:pk>/eliminar/', views.cliente_eliminar, name='cliente_eliminar'),

    path('cuentas/', views.cuenta_lista, name='cuenta_lista'),
    path('cuentas/nueva/', views.cuenta_crear, name='cuenta_crear'),
    path('cuentas/<int:pk>/editar/', views.cuenta_editar, name='cuenta_editar'),
    path('cuentas/<int:pk>/eliminar/', views.cuenta_eliminar, name='cuenta_eliminar'),

    path('transacciones/', views.transaccion_lista, name='transaccion_lista'),
    path('transacciones/nueva/', views.transaccion_crear, name='transaccion_crear'),

    path('reportes/saldos/', views.reporte_saldos, name='reporte_saldos'),
]
