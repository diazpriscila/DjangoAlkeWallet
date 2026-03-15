from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    # lo vinculo al usuario de django para el login
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    rut = models.CharField(max_length=15, unique=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


class Cuenta(models.Model):

    TIPOS_CUENTA = [
        ('ahorro', 'Caja de Ahorro'),
        ('corriente', 'Cuenta Corriente'),
        ('digital', 'Billetera Digital'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='cuentas')
    tipo = models.CharField(max_length=20, choices=TIPOS_CUENTA, default='digital')
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    activa = models.BooleanField(default=True)
    fecha_apertura = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.cliente.nombre} | {self.get_tipo_display()} | saldo: ${self.saldo}'

    class Meta:
        ordering = ['-fecha_apertura']


class Transaccion(models.Model):

    TIPOS_TX = [
        ('deposito', 'Depósito'),
        ('extraccion', 'Extracción'),
        ('transferencia', 'Transferencia'),
    ]

    cuenta_origen = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='transacciones_enviadas')
    # destino es opcional, solo aplica en transferencias
    cuenta_destino = models.ForeignKey(Cuenta, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacciones_recibidas')
    tipo = models.CharField(max_length=20, choices=TIPOS_TX)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    descripcion = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.get_tipo_display()} - ${self.monto}'

    class Meta:
        ordering = ['-fecha']
