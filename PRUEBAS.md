# Informe de pruebas — Alke Wallet

## Pruebas manuales realizadas

| Funcionalidad | Acción | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|
| Login | Ingresar con usuario y contraseña correctos | Redirige a lista de clientes | Redirige correctamente | ✅ |
| Login | Ingresar con contraseña incorrecta | Muestra mensaje de error | Muestra error en el formulario | ✅ |
| Login | Acceder a `/clientes/` sin sesión iniciada | Redirige al login | Redirige al login | ✅ |
| Crear cliente | Completar formulario con datos válidos | Cliente aparece en la lista | Cliente guardado correctamente | ✅ |
| Crear cliente | Enviar formulario con email duplicado | Muestra error de validación | Error en campo email | ✅ |
| Crear cliente | Enviar formulario con RUT duplicado | Muestra error de validación | Error en campo rut | ✅ |
| Editar cliente | Modificar teléfono y guardar | Dato actualizado en la lista | Cambio guardado correctamente | ✅ |
| Eliminar cliente | Confirmar eliminación | Cliente desaparece de la lista | Cliente eliminado | ✅ |
| Eliminar cliente | Cancelar eliminación | No se elimina nada | Vuelve sin cambios | ✅ |
| Crear cuenta | Asociar cuenta a un cliente | Cuenta aparece en la lista | Cuenta creada correctamente | ✅ |
| Desactivar cuenta | Confirmar desactivación | Cuenta desaparece de la lista activa | Cuenta marcada como inactiva | ✅ |
| Depósito | Registrar depósito en una cuenta | Saldo de la cuenta aumenta | Saldo actualizado correctamente | ✅ |
| Extracción | Registrar extracción con saldo suficiente | Saldo de la cuenta disminuye | Saldo actualizado correctamente | ✅ |
| Extracción | Registrar extracción con saldo insuficiente | Muestra error de saldo insuficiente | Mensaje de error mostrado | ✅ |
| Transferencia | Transferir entre dos cuentas | Saldo origen baja, saldo destino sube | Ambos saldos actualizados | ✅ |
| Transferencia | Transferir sin indicar cuenta destino | Muestra error | Mensaje de error mostrado | ✅ |
| Reporte de saldos | Ingresar a `/reportes/saldos/` | Tabla con saldo total por cliente | Reporte generado correctamente | ✅ |
| Admin | Acceder a `/admin/` con superusuario | Ver modelos registrados | Cliente, Cuenta y Transaccion visibles | ✅ |
| Admin | Buscar cliente por nombre | Filtra resultados | Búsqueda funciona correctamente | ✅ |

## Consultas SQL personalizadas probadas

| Consulta | Método | Resultado |
|---|---|---|
| Saldo total agrupado por cliente con JOIN | `raw()` | Devuelve lista ordenada por saldo descendente ✅ |
| Conteo total de transacciones | `connection.cursor()` | Devuelve número correcto de registros ✅ |
| Filtro de clientes por nombre o email | `filter()` con `icontains` | Resultados correctos con búsqueda parcial ✅ |
| Anotación de cantidad de cuentas por cliente | `annotate()` con `Count` | Muestra cantidad correcta en la lista ✅ |

## Validaciones comprobadas

- Todos los formularios incluyen `{% csrf_token %}` ✅
- Todas las vistas están protegidas con `@login_required` ✅
- Las cuentas no se eliminan físicamente, se desactivan ✅
- Las transferencias validan saldo antes de ejecutarse ✅
- Los campos `email` y `rut` son únicos por cliente ✅

## Observaciones

- La app fue probada en entorno de desarrollo con SQLite
- Se usó Bootstrap 5 cargado desde CDN, requiere conexión a internet para los estilos
- El reporte de saldos solo muestra clientes con cuentas activas
