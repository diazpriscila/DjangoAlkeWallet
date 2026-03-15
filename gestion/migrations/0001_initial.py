from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('email', models.EmailField(unique=True)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('dni', models.CharField(max_length=15, unique=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('ahorro', 'Caja de Ahorro'), ('corriente', 'Cuenta Corriente'), ('digital', 'Billetera Digital')], default='digital', max_length=20)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('activa', models.BooleanField(default=True)),
                ('fecha_apertura', models.DateField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuentas', to='gestion.cliente')),
            ],
            options={
                'ordering': ['-fecha_apertura'],
            },
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('deposito', 'Depósito'), ('extraccion', 'Extracción'), ('transferencia', 'Transferencia')], max_length=20)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=12)),
                ('descripcion', models.TextField(blank=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('cuenta_destino', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transacciones_recibidas', to='gestion.cuenta')),
                ('cuenta_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transacciones_enviadas', to='gestion.cuenta')),
            ],
            options={
                'ordering': ['-fecha'],
            },
        ),
    ]
