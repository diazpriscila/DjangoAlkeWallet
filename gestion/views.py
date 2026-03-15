from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import connection
from django.db.models import Sum, Count
from .models import Cliente, Cuenta, Transaccion
from .forms import ClienteForm, CuentaForm, TransaccionForm


@login_required
def dashboard(request):
    # resumen general para el panel principal
    total_clientes = Cliente.objects.count()
    total_cuentas = Cuenta.objects.filter(activa=True).count()
    total_transacciones = Transaccion.objects.count()

    saldo_total = Cuenta.objects.aggregate(total=Sum('saldo'))['total']
    if saldo_total is None:
        saldo_total = 0

    ultimas_transacciones = Transaccion.objects.select_related('cuenta_origen__cliente')[:5]

    context = {
        'total_clientes': total_clientes,
        'total_cuentas': total_cuentas,
        'total_transacciones': total_transacciones,
        'saldo_total': saldo_total,
        'ultimas_transacciones': ultimas_transacciones,
    }
    return render(request, 'gestion/dashboard.html', context)


# ---- Clientes ----

@login_required
def cliente_lista(request):
    busqueda = request.GET.get('q', '')
    clientes = Cliente.objects.annotate(cantidad_cuentas=Count('cuentas'))

    if busqueda:
        por_nombre = clientes.filter(nombre__icontains=busqueda)
        por_email = clientes.filter(email__icontains=busqueda)
        clientes = (por_nombre | por_email).distinct()

    return render(request, 'gestion/cliente_lista.html', {
        'clientes': clientes,
        'busqueda': busqueda
    })


@login_required
def cliente_detalle(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cuentas = cliente.cuentas.all()
    return render(request, 'gestion/cliente_detalle.html', {
        'cliente': cliente,
        'cuentas': cuentas
    })


@login_required
def cliente_crear(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente creado correctamente.')
            return redirect('cliente_lista')
    else:
        form = ClienteForm()

    return render(request, 'gestion/cliente_form.html', {
        'form': form,
        'titulo': 'Nuevo Cliente'
    })


@login_required
def cliente_editar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado.')
            return redirect('cliente_lista')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'gestion/cliente_form.html', {
        'form': form,
        'titulo': 'Editar Cliente'
    })


@login_required
def cliente_eliminar(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado.')
        return redirect('cliente_lista')

    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': cliente,
        'tipo': 'cliente'
    })


# ---- Cuentas ----

@login_required
def cuenta_lista(request):
    # solo muestro las activas
    cuentas = Cuenta.objects.select_related('cliente').filter(activa=True)
    return render(request, 'gestion/cuenta_lista.html', {'cuentas': cuentas})


@login_required
def cuenta_crear(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada.')
            return redirect('cuenta_lista')
    else:
        form = CuentaForm()

    return render(request, 'gestion/cuenta_form.html', {
        'form': form,
        'titulo': 'Nueva Cuenta'
    })


@login_required
def cuenta_editar(request, pk):
    cuenta = get_object_or_404(Cuenta, pk=pk)

    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta actualizada.')
            return redirect('cuenta_lista')
    else:
        form = CuentaForm(instance=cuenta)

    return render(request, 'gestion/cuenta_form.html', {
        'form': form,
        'titulo': 'Editar Cuenta'
    })


@login_required
def cuenta_eliminar(request, pk):
    cuenta = get_object_or_404(Cuenta, pk=pk)
    if request.method == 'POST':
        # no la borro fisicamente, la desactivo nomás
        cuenta.activa = False
        cuenta.save()
        messages.success(request, 'Cuenta desactivada.')
        return redirect('cuenta_lista')

    return render(request, 'gestion/confirmar_eliminar.html', {
        'objeto': cuenta,
        'tipo': 'cuenta'
    })


# ---- Transacciones ----

@login_required
def transaccion_lista(request):
    transacciones = Transaccion.objects.select_related('cuenta_origen__cliente')
    return render(request, 'gestion/transaccion_lista.html', {'transacciones': transacciones})


@login_required
def transaccion_crear(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción registrada.')
            return redirect('transaccion_lista')
    else:
        form = TransaccionForm()

    return render(request, 'gestion/transaccion_form.html', {
        'form': form,
        'titulo': 'Nueva Transacción'
    })


# ---- Reporte con SQL personalizado ----

@login_required
def reporte_saldos(request):
    # uso raw() para hacer el join y agrupar saldo por cliente
    clientes_con_saldo = Cliente.objects.raw("""
        SELECT c.id, c.nombre, c.email, SUM(cu.saldo) as saldo_total
        FROM gestion_cliente c
        JOIN gestion_cuenta cu ON cu.cliente_id = c.id
        WHERE cu.activa = 1
        GROUP BY c.id, c.nombre, c.email
        ORDER BY saldo_total DESC
    """)

    # también pruebo con cursor directo para contar operaciones
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM gestion_transaccion")
        total_ops = cursor.fetchone()[0]

    return render(request, 'gestion/reporte_saldos.html', {
        'clientes': clientes_con_saldo,
        'total_ops': total_ops,
    })
