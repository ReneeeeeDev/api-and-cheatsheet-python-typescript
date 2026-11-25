# 20 ejercicios extra (31–50): lógica aplicada a problemas reales

Soluciones: `soluciones_extra.py` y `soluciones_extra.js` (mismos nombres; en JS en camelCase).
Ejecutar las pruebas: `python soluciones_extra.py` · `node soluciones_extra.js`.

**Cómo practicar:** lee el enunciado, escribe la función en un archivo nuevo, pruébala con los ejemplos y **solo después** compara con la solución. Anota cuánto tardaste.

---

### 31. RUC de persona natural — ⭐
`validar_ruc_natural(ruc)`: en Ecuador, el RUC de una persona natural tiene 13 dígitos: su cédula (válida) + `001`.
`"1710034065001"` → True · `"1710034065002"` → False

### 32. Factura con descuento e IVA — ⭐⭐
`calcular_factura(items)` donde items = `[(descripcion, cantidad, precio_unitario)]`.
Si el subtotal **supera** $100, aplica 10 % de descuento. El IVA (15 %) se calcula sobre el subtotal con descuento. Redondea a 2 decimales.
Devuelve `{subtotal, descuento, base, iva, total}`.
`[("Mouse", 2, 15), ("Teclado", 1, 45)]` → subtotal 75, descuento 0, iva 11.25, total 86.25
`[("Monitor", 1, 200)]` → descuento 20, base 180, iva 27, total 207

### 33. Estadísticas de notas — ⭐⭐
`estadisticas(notas)` → `{min, max, promedio (2 dec.), mediana, moda}`. La mediana, con n par, es el promedio de los dos del centro. Si hay empate en la moda, devuelve la menor.
`[7, 9, 8, 9, 6, 7]` → min 6, max 9, promedio 7.67, mediana 7.5, moda 7

### 34. Segundos a HH:MM:SS — ⭐
`3725` → `"01:02:05"`

### 35. Detectar reservas en conflicto — ⭐⭐
`reservas_en_conflicto(reservas)`, reservas = `[(id, laboratorio, "HH:MM" inicio, "HH:MM" fin)]` del mismo día. Devuelve los pares `(id1, id2)` del **mismo laboratorio** cuyos horarios se cruzan (los contiguos no chocan).
`[(1,"L1","08:00","10:00"), (2,"L1","09:00","11:00"), (3,"L2","08:00","10:00"), (4,"L1","10:00","12:00")]` → `[(1, 2), (2, 4)]`

### 36. Fusionar intervalos — ⭐⭐⭐ (clásico de entrevistas)
`[[14,15],[8,10],[9,12],[12,13]]` → `[[8,13],[14,15]]`.
Pista: ordena por inicio; si el siguiente empieza antes o justo cuando termina el último, amplía el último.

### 37. Letras más frecuentes — ⭐⭐
`top_caracteres(texto, n=3)`: ignora mayúsculas y lo que no sea letra. En caso de empate, orden alfabético.
`"Desarrollo de Software"` → `[("e",3), ("o",3), ("r",3)]`

### 38. Matriz en espiral — ⭐⭐⭐
`matriz_espiral(3)` → `[[1,2,3],[8,9,4],[7,6,5]]`
Pista: 4 límites (arriba, abajo, izquierda, derecha) que se van cerrando.

### 39. Validar contraseña con mensajes — ⭐⭐
`validar_password(clave)` devuelve la **lista de reglas incumplidas**: mínimo 8 caracteres, una mayúscula, una minúscula, un número, un símbolo y sin espacios.
`"Clave#2026"` → `[]` · `"abc"` → 4 errores

### 40. Número a letras — ⭐⭐⭐ (para facturas y cheques)
`numero_a_letras(n)` para 0 ≤ n < 1 000 000.
`1995` → `"mil novecientos noventa y cinco"` · `100` → `"cien"` · `115` → `"ciento quince"` · `21000` → `"veintiun mil"`
Pista: casos < 30 en tabla, decenas "y", centenas, y recursión para los miles.

### 41. Multiplicar matrices — ⭐⭐
`[[1,2],[3,4]] × [[5,6],[7,8]]` → `[[19,22],[43,50]]`. Lanza error si las dimensiones no son compatibles.

### 42. Rotar lista — ⭐
Rotar a la derecha k posiciones: `[1,2,3,4,5], 2` → `[4,5,1,2,3]`. Con k mayor que la longitud usa el residuo.

### 43. Agrupar anagramas — ⭐⭐
`["amor","gato","Roma","toga","ramo","sol"]` → `[["amor","Roma","ramo"],["gato","toga"],["sol"]]` (grupos más grandes primero).
Pista: la clave de cada grupo es la palabra con sus letras ordenadas.

### 44. Cambio mínimo de monedas — ⭐⭐⭐ (programación dinámica)
`cambio_minimo(monto, monedas)`: mínima cantidad de monedas; -1 si es imposible.
`cambio_minimo(30, (1, 10, 25))` → 3 (10+10+10). El método "greedy" daría 6 (25+1+1+1+1+1): por eso se necesita programación dinámica.
`cambio_minimo(63)` con (1,5,10,25,50) → 5 · `cambio_minimo(3, (2,))` → -1

### 45. Fecha válida — ⭐⭐
`fecha_valida(dia, mes, anio)` considerando años bisiestos.
`(29, 2, 2024)` → True · `(29, 2, 2026)` → False · `(31, 4, 2026)` → False

### 46. Días hábiles entre fechas — ⭐⭐
Cuenta lunes a viernes entre dos fechas (inclusive), excluyendo los feriados recibidos.
Del 21/09/2026 al 02/10/2026 → 10 · del 05/10 al 11/10 con feriado el 09/10 → 4

### 47. Cuota de préstamo (sistema francés) — ⭐⭐
`cuota_prestamo(monto, tasa_anual, meses)`: `C = P·i / (1 − (1+i)^−n)`, con `i = tasa_anual / 12`.
`(5000, 0.12, 12)` → 444.24. Extra: `tabla_amortizacion` con mes, cuota, interés, capital y saldo.

### 48. Primer carácter no repetido — ⭐
`"aabbcdc"` → `"d"` · `"aa"` → None

### 49. Reorden de inventario — ⭐⭐
Productos `{codigo, stock, venta_diaria}`. Hay que pedir si el stock no cubre 15 días de venta. La cantidad a pedir es la necesaria para tener el **doble** de cobertura (30 días) menos el stock actual. Devuelve `[(codigo, cantidad)]` ordenado de mayor a menor cantidad.
`[{"A", stock 10, venta 2}, {"B", stock 100, venta 1}]` → `[("A", 50)]`

### 50. Sistema de calificaciones — ⭐⭐
`sistema_notas(parciales, examen, asistencia)`: nota final = 60 % del promedio de parciales + 40 % del examen. Reglas, en este orden: asistencia < 70 % → "Reprobado por asistencia"; final ≥ 7 → "Aprobado"; ≥ 5 → "Supletorio"; si no → "Reprobado".
`([8,7,9], 6, 90)` → `(7.2, "Aprobado")`

---

## Retos de consola (programas completos, sin solución: para practicar en 20–30 min cada uno)
1. **Cajero automático:** menú de consultar saldo, depositar, retirar (sin saldo negativo, máximo $500 por retiro), historial y salir.
2. **Agenda de contactos** en archivo JSON: agregar, buscar por nombre, editar, eliminar y listar ordenado.
3. **Juego adivina el número:** número aleatorio del 1 al 100, pistas "mayor/menor", contador de intentos y récord guardado en archivo.
4. **Conversor de unidades** con menú: temperatura, longitud y moneda (tasas en un diccionario).
5. **Registro de notas de un curso:** ingresar estudiantes y 3 notas; mostrar la tabla con promedio, el mejor, los reprobados y el promedio del curso.
