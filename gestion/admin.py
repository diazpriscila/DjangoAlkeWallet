from django.contrib import admin
from .models import Cliente, Cuenta, Transaccion


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'rut', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'email', 'rut')


@admin.register(Cuenta)
class CuentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'tipo', 'saldo', 'activa')
    list_filter = ('tipo', 'activa')


@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ('cuenta_origen', 'tipo', 'monto', 'fecha')
    list_filter = ('tipo',)
