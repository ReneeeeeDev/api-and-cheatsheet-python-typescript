"""Soluciones de los 20 ejercicios extra (31 a 50). Enunciados en ejercicios_extra.md.
Ejecutar:  python soluciones_extra.py   (corre las pruebas al final)
"""
from collections import Counter, defaultdict
from datetime import date


# ------------------------------------------------------------------ 31
def validar_ruc_natural(ruc):
    """RUC de persona natural en Ecuador = cédula válida + '001'."""
    if len(ruc) != 13 or not ruc.isdigit() or not ruc.endswith("001"):
        return False
    return validar_cedula(ruc[:10])


def validar_cedula(c):
    if len(c) != 10 or not c.isdigit():
        return False
    prov = int(c[:2])
    if not (1 <= prov <= 24 or prov == 30) or int(c[2]) >= 6:
        return False
    suma = sum((d - 9 if d > 9 else d) for d in (int(c[i]) * (2 if i % 2 == 0 else 1) for i in range(9)))
    return (10 - suma % 10) % 10 == int(c[9])


# ------------------------------------------------------------------ 32
def calcular_factura(items, tasa_iva=0.15, descuento_desde=100, descuento=0.10):
    """items: [(descripcion, cantidad, precio_unitario)].
    Descuento del 10 % sobre el subtotal si supera 100. IVA sobre el subtotal con descuento."""
    subtotal = round(sum(c * p for _, c, p in items), 2)
    desc = round(subtotal * descuento, 2) if subtotal > descuento_desde else 0.0
    base = round(subtotal - desc, 2)
    iva = round(base * tasa_iva, 2)
    return {"subtotal": subtotal, "descuento": desc, "base": base, "iva": iva, "total": round(base + iva, 2)}


# ------------------------------------------------------------------ 33
def estadisticas(notas):
    """min, max, promedio, mediana y moda (la menor si hay empate)."""
    ordenadas = sorted(notas)
    n = len(ordenadas)
    medio = n // 2
    mediana = ordenadas[medio] if n % 2 else (ordenadas[medio - 1] + ordenadas[medio]) / 2
    conteo = Counter(ordenadas)
    max_rep = max(conteo.values())
    moda = min(v for v, c in conteo.items() if c == max_rep)
    return {"min": ordenadas[0], "max": ordenadas[-1], "promedio": round(sum(notas) / n, 2),
            "mediana": mediana, "moda": moda}


# ------------------------------------------------------------------ 34
def segundos_a_hms(segundos):
    h, resto = divmod(segundos, 3600)
    m, s = divmod(resto, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"


# ------------------------------------------------------------------ 35
def reservas_en_conflicto(reservas):
    """reservas: [(id, lab, inicio 'HH:MM', fin 'HH:MM')] del mismo día.
    Devuelve pares (id1, id2) que se cruzan en el mismo laboratorio."""
    conflictos = []
    for i in range(len(reservas)):
        for j in range(i + 1, len(reservas)):
            a, b = reservas[i], reservas[j]
            if a[1] == b[1] and a[2] < b[3] and b[2] < a[3]:
                conflictos.append((a[0], b[0]))
    return conflictos


# ------------------------------------------------------------------ 36
def fusionar_intervalos(intervalos):
    """[[8,10],[9,12],[14,15]] → [[8,12],[14,15]]. Ordena y une los que se solapan o tocan."""
    resultado = []
    for inicio, fin in sorted(intervalos):
        if resultado and inicio <= resultado[-1][1]:
            resultado[-1][1] = max(resultado[-1][1], fin)
        else:
            resultado.append([inicio, fin])
    return resultado


# ------------------------------------------------------------------ 37
def top_caracteres(texto, n=3):
    """Las n letras más frecuentes (ignora espacios, mayúsculas); empate → orden alfabético."""
    conteo = Counter(c for c in texto.lower() if c.isalpha())
    return sorted(conteo.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


# ------------------------------------------------------------------ 38
def matriz_espiral(n):
    """Matriz n×n con 1..n² en espiral horaria."""
    m = [[0] * n for _ in range(n)]
    arriba, abajo, izq, der = 0, n - 1, 0, n - 1
    valor = 1
    while arriba <= abajo and izq <= der:
        for c in range(izq, der + 1):
            m[arriba][c] = valor; valor += 1
        arriba += 1
        for f in range(arriba, abajo + 1):
            m[f][der] = valor; valor += 1
        der -= 1
        if arriba <= abajo:
            for c in range(der, izq - 1, -1):
                m[abajo][c] = valor; valor += 1
            abajo -= 1
        if izq <= der:
            for f in range(abajo, arriba - 1, -1):
                m[f][izq] = valor; valor += 1
            izq += 1
    return m


# ------------------------------------------------------------------ 39
def validar_password(clave):
    """Devuelve la lista de reglas incumplidas (vacía = válida)."""
    errores = []
    if len(clave) < 8:
        errores.append("mínimo 8 caracteres")
    if not any(c.isupper() for c in clave):
        errores.append("una mayúscula")
    if not any(c.islower() for c in clave):
        errores.append("una minúscula")
    if not any(c.isdigit() for c in clave):
        errores.append("un número")
    if not any(not c.isalnum() for c in clave):
        errores.append("un símbolo")
    if " " in clave:
        errores.append("sin espacios")
    return errores


# ------------------------------------------------------------------ 40
UNIDADES = ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez",
            "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve",
            "veinte", "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco", "veintiséis",
            "veintisiete", "veintiocho", "veintinueve"]
DECENAS = ["", "", "", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"]
CENTENAS = ["", "ciento", "doscientos", "trescientos", "cuatrocientos", "quinientos", "seiscientos",
            "setecientos", "ochocientos", "novecientos"]


def numero_a_letras(n):
    """0 a 999 999 en palabras (útil para facturas y cheques)."""
    if n < 30:
        return UNIDADES[n]
    if n < 100:
        d, u = divmod(n, 10)
        return DECENAS[d] + ("" if u == 0 else " y " + UNIDADES[u])
    if n < 1000:
        c, resto = divmod(n, 100)
        if n == 100:
            return "cien"
        return CENTENAS[c] + ("" if resto == 0 else " " + numero_a_letras(resto))
    miles, resto = divmod(n, 1000)
    prefijo = "mil" if miles == 1 else numero_a_letras(miles).replace("uno", "un") + " mil"
    return prefijo + ("" if resto == 0 else " " + numero_a_letras(resto))


# ------------------------------------------------------------------ 41
def multiplicar_matrices(a, b):
    if len(a[0]) != len(b):
        raise ValueError("Columnas de A deben ser iguales a filas de B")
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


# ------------------------------------------------------------------ 42
def rotar_lista(lista, k):
    """Rota a la derecha k posiciones: [1,2,3,4,5], 2 → [4,5,1,2,3]."""
    if not lista:
        return []
    k %= len(lista)
    return lista[-k:] + lista[:-k] if k else lista[:]


# ------------------------------------------------------------------ 43
def agrupar_anagramas(palabras):
    grupos = defaultdict(list)
    for p in palabras:
        grupos["".join(sorted(p.lower()))].append(p)
    return sorted(grupos.values(), key=lambda g: (-len(g), g[0]))


# ------------------------------------------------------------------ 44
def cambio_minimo(monto, monedas=(1, 5, 10, 25, 50)):
    """Programación dinámica: mínima cantidad de monedas (funciona aunque el método 'greedy' falle).
    Devuelve -1 si no se puede."""
    INF = float("inf")
    minimo = [0] + [INF] * monto
    for valor in range(1, monto + 1):
        for m in monedas:
            if m <= valor and minimo[valor - m] + 1 < minimo[valor]:
                minimo[valor] = minimo[valor - m] + 1
    return -1 if minimo[monto] == INF else minimo[monto]


# ------------------------------------------------------------------ 45
def fecha_valida(dia, mes, anio):
    if anio < 1 or not 1 <= mes <= 12 or dia < 1:
        return False
    bisiesto = (anio % 4 == 0 and anio % 100 != 0) or anio % 400 == 0
    dias_mes = [31, 29 if bisiesto else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return dia <= dias_mes[mes - 1]


# ------------------------------------------------------------------ 46
def dias_habiles_entre(desde, hasta, feriados=()):
    """Cuenta lunes a viernes entre dos fechas (inclusive), excluyendo feriados."""
    total = 0
    dia = desde
    while dia <= hasta:
        if dia.weekday() < 5 and dia not in feriados:
            total += 1
        dia = date.fromordinal(dia.toordinal() + 1)
    return total


# ------------------------------------------------------------------ 47
def cuota_prestamo(monto, tasa_anual, meses):
    """Sistema francés (cuota fija): C = P·i / (1 − (1+i)^−n), i = tasa mensual."""
    i = tasa_anual / 12
    if i == 0:
        return round(monto / meses, 2)
    return round(monto * i / (1 - (1 + i) ** -meses), 2)


def tabla_amortizacion(monto, tasa_anual, meses):
    cuota = cuota_prestamo(monto, tasa_anual, meses)
    saldo = monto
    filas = []
    for mes in range(1, meses + 1):
        interes = round(saldo * tasa_anual / 12, 2)
        capital = round(cuota - interes, 2) if mes < meses else round(saldo, 2)
        saldo = round(saldo - capital, 2)
        filas.append((mes, cuota if mes < meses else round(capital + interes, 2), interes, capital, max(saldo, 0)))
    return filas


# ------------------------------------------------------------------ 48
def primer_no_repetido(texto):
    conteo = Counter(texto)
    return next((c for c in texto if conteo[c] == 1), None)


# ------------------------------------------------------------------ 49
def reorden_inventario(productos, dias_cobertura=15):
    """productos: [{"codigo", "stock", "venta_diaria"}].
    Pedir si el stock no cubre 'dias_cobertura'. Cantidad = lo necesario para cubrir el doble."""
    pedidos = []
    for p in productos:
        necesario = p["venta_diaria"] * dias_cobertura
        if p["stock"] < necesario:
            pedidos.append((p["codigo"], p["venta_diaria"] * dias_cobertura * 2 - p["stock"]))
    return sorted(pedidos, key=lambda x: -x[1])


# ------------------------------------------------------------------ 50
def sistema_notas(parciales, examen, asistencia):
    """Nota final = 60 % promedio de parciales + 40 % examen.
    Reprueba por asistencia < 70 %. Supletorio si la final está entre 5 y 6.99."""
    promedio = sum(parciales) / len(parciales)
    final = round(promedio * 0.6 + examen * 0.4, 2)
    if asistencia < 70:
        estado = "Reprobado por asistencia"
    elif final >= 7:
        estado = "Aprobado"
    elif final >= 5:
        estado = "Supletorio"
    else:
        estado = "Reprobado"
    return final, estado


# ================================================================== PRUEBAS
if __name__ == "__main__":
    casos = [
        (validar_ruc_natural("1710034065001") and not validar_ruc_natural("1710034065002"), "31 ruc"),
        (calcular_factura([("Mouse", 2, 15), ("Teclado", 1, 45)]) ==
         {"subtotal": 75, "descuento": 0.0, "base": 75, "iva": 11.25, "total": 86.25}, "32 factura sin desc"),
        (calcular_factura([("Monitor", 1, 200)])["total"] == 207.0, "32 factura con desc"),
        (estadisticas([7, 9, 8, 9, 6, 7]) == {"min": 6, "max": 9, "promedio": 7.67, "mediana": 7.5, "moda": 7}, "33 estadisticas"),
        (segundos_a_hms(3725) == "01:02:05", "34 hms"),
        (reservas_en_conflicto([(1, "L1", "08:00", "10:00"), (2, "L1", "09:00", "11:00"),
                                (3, "L2", "08:00", "10:00"), (4, "L1", "10:00", "12:00")]) == [(1, 2), (2, 4)], "35 conflictos"),
        (fusionar_intervalos([[14, 15], [8, 10], [9, 12], [12, 13]]) == [[8, 13], [14, 15]], "36 fusionar"),
        (top_caracteres("Desarrollo de Software") == [("e", 3), ("o", 3), ("r", 3)], "37 top"),
        (matriz_espiral(3) == [[1, 2, 3], [8, 9, 4], [7, 6, 5]], "38 espiral"),
        (validar_password("Clave#2026") == [] and len(validar_password("abc")) == 4, "39 password"),
        (numero_a_letras(1995) == "mil novecientos noventa y cinco" and numero_a_letras(21000) == "veintiun mil"
         and numero_a_letras(100) == "cien" and numero_a_letras(115) == "ciento quince", "40 letras"),
        (multiplicar_matrices([[1, 2], [3, 4]], [[5, 6], [7, 8]]) == [[19, 22], [43, 50]], "41 matrices"),
        (rotar_lista([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3] and rotar_lista([1, 2], 4) == [1, 2], "42 rotar"),
        (agrupar_anagramas(["amor", "gato", "Roma", "toga", "ramo", "sol"]) ==
         [["amor", "Roma", "ramo"], ["gato", "toga"], ["sol"]], "43 anagramas"),
        (cambio_minimo(30, (1, 10, 25)) == 3 and cambio_minimo(63) == 5 and cambio_minimo(3, (2,)) == -1, "44 cambio"),
        (fecha_valida(29, 2, 2024) and not fecha_valida(29, 2, 2026) and not fecha_valida(31, 4, 2026), "45 fecha"),
        (dias_habiles_entre(date(2026, 9, 21), date(2026, 10, 2)) == 10
         and dias_habiles_entre(date(2026, 10, 5), date(2026, 10, 11), {date(2026, 10, 9)}) == 4, "46 habiles"),
        (cuota_prestamo(5000, 0.12, 12) == 444.24 and tabla_amortizacion(5000, 0.12, 12)[-1][4] == 0, "47 prestamo"),
        (primer_no_repetido("aabbcdc") == "d" and primer_no_repetido("aa") is None, "48 no repetido"),
        (reorden_inventario([{"codigo": "A", "stock": 10, "venta_diaria": 2},
                             {"codigo": "B", "stock": 100, "venta_diaria": 1}]) == [("A", 50)], "49 reorden"),
        (sistema_notas([8, 7, 9], 6, 90) == (7.2, "Aprobado") and sistema_notas([5, 6], 5, 80)[1] == "Supletorio"
         and sistema_notas([10], 10, 60)[1] == "Reprobado por asistencia", "50 notas"),
    ]
    for ok, nombre in casos:
        print(("OK    " if ok else "FALLO ") + nombre)
    print(f"\n{sum(ok for ok, _ in casos)}/{len(casos)} correctas")
    print("\nTabla de amortización $5000 al 12% anual, 12 meses:")
    print(f"{'Mes':>3} {'Cuota':>9} {'Interés':>9} {'Capital':>9} {'Saldo':>10}")
    for fila in tabla_amortizacion(5000, 0.12, 12):
        print(f"{fila[0]:>3} {fila[1]:>9.2f} {fila[2]:>9.2f} {fila[3]:>9.2f} {fila[4]:>10.2f}")
    print("\n" + "\n".join(" ".join(f"{x:3d}" for x in fila) for fila in matriz_espiral(4)))
