"""Pruebas de los 30 problemas de PROBLEMAS.md.

Uso (desde esta carpeta):
    python pruebas.py                       # prueba las soluciones de referencia
    python pruebas.py mis_soluciones        # prueba TU archivo (copia plantilla.py → mis_soluciones.py)
    python pruebas.py mis_soluciones 7 12   # solo los problemas 7 y 12

Las funciones que siguen con `raise NotImplementedError` aparecen como PENDIENTE.
"""
import importlib
import sys

from estructuras import crear_arbol, crear_lista, lista_a_python

PRUEBAS = []


def prueba(numero, nombre):
    def registrar(funcion):
        PRUEBAS.append((numero, nombre, funcion))
        return funcion
    return registrar


def igual(obtenido, esperado):
    if obtenido != esperado:
        raise AssertionError(f"se esperaba {esperado!r}, se obtuvo {obtenido!r}")


def normalizar(listas):
    """Para resultados cuyo orden no importa (tripletas, subconjuntos)."""
    return sorted(sorted(x) for x in listas)


# ---------------------------------------------------------------- A. hash
@prueba(1, "contiene_duplicado")
def _(m):
    igual(m.contiene_duplicado([1, 2, 3, 1]), True)
    igual(m.contiene_duplicado([1, 2, 3, 4]), False)
    igual(m.contiene_duplicado([]), False)


@prueba(2, "elemento_mayoritario")
def _(m):
    igual(m.elemento_mayoritario([3, 2, 3]), 3)
    igual(m.elemento_mayoritario([2, 2, 1, 1, 1, 2, 2]), 2)
    igual(m.elemento_mayoritario([1, 5, 5]), 5)
    igual(m.elemento_mayoritario([7]), 7)


@prueba(3, "secuencia_consecutiva_mas_larga")
def _(m):
    igual(m.secuencia_consecutiva_mas_larga([100, 4, 200, 1, 3, 2]), 4)
    igual(m.secuencia_consecutiva_mas_larga([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]), 9)
    igual(m.secuencia_consecutiva_mas_larga([]), 0)


@prueba(4, "subarreglos_suma_k")
def _(m):
    igual(m.subarreglos_suma_k([1, 1, 1], 2), 2)
    igual(m.subarreglos_suma_k([1, 2, 3], 3), 2)
    igual(m.subarreglos_suma_k([1, -1, 0], 0), 3)


@prueba(5, "producto_excepto_si_mismo")
def _(m):
    igual(m.producto_excepto_si_mismo([1, 2, 3, 4]), [24, 12, 8, 6])
    igual(m.producto_excepto_si_mismo([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0])
    igual(m.producto_excepto_si_mismo([0, 1, 2]), [2, 0, 0])


# ----------------------------------------------------------- B. punteros
@prueba(6, "mover_ceros")
def _(m):
    nums = [0, 1, 0, 3, 12]
    m.mover_ceros(nums)
    igual(nums, [1, 3, 12, 0, 0])           # debe modificar la misma lista
    nums = [0, 0, 1]
    m.mover_ceros(nums)
    igual(nums, [1, 0, 0])


@prueba(7, "fusionar_ordenadas")
def _(m):
    igual(m.fusionar_ordenadas([1, 3, 5], [2, 4]), [1, 2, 3, 4, 5])
    igual(m.fusionar_ordenadas([], [1]), [1])
    igual(m.fusionar_ordenadas([1, 1], [1]), [1, 1, 1])


@prueba(8, "tres_suma")
def _(m):
    igual(normalizar(m.tres_suma([-1, 0, 1, 2, -1, -4])), [[-1, -1, 2], [-1, 0, 1]])
    igual(normalizar(m.tres_suma([0, 0, 0, 0])), [[0, 0, 0]])
    igual(m.tres_suma([1, 2, 3]), [])


@prueba(9, "contenedor_mas_agua")
def _(m):
    igual(m.contenedor_mas_agua([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)
    igual(m.contenedor_mas_agua([1, 1]), 1)


# ------------------------------------------------------------- C. ventana
@prueba(10, "max_suma_ventana")
def _(m):
    igual(m.max_suma_ventana([2, 1, 5, 1, 3, 2], 3), 9)
    igual(m.max_suma_ventana([-1, -2, -3], 2), -3)
    igual(m.max_suma_ventana([1, 2], 3), None)


@prueba(11, "subcadena_sin_repetir")
def _(m):
    igual(m.subcadena_sin_repetir("abcabcbb"), 3)
    igual(m.subcadena_sin_repetir("bbbbb"), 1)
    igual(m.subcadena_sin_repetir("pwwkew"), 3)
    igual(m.subcadena_sin_repetir("abba"), 2)
    igual(m.subcadena_sin_repetir(""), 0)


# --------------------------------------------------------------- D. pilas
@prueba(12, "evaluar_rpn")
def _(m):
    igual(m.evaluar_rpn(["2", "1", "+", "3", "*"]), 9)
    igual(m.evaluar_rpn(["4", "13", "5", "/", "+"]), 6)
    igual(m.evaluar_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]), 22)


@prueba(13, "temperaturas_diarias")
def _(m):
    igual(m.temperaturas_diarias([73, 74, 75, 71, 69, 72, 76, 73]), [1, 1, 4, 2, 1, 1, 0, 0])
    igual(m.temperaturas_diarias([30, 60, 90]), [1, 1, 0])
    igual(m.temperaturas_diarias([90, 60, 30]), [0, 0, 0])


@prueba(14, "PilaMinima")
def _(m):
    p = m.PilaMinima()
    p.apilar(5)
    p.apilar(3)
    p.apilar(7)
    p.apilar(3)
    igual(p.minimo(), 3)
    igual(p.desapilar(), 3)
    igual(p.minimo(), 3)
    p.desapilar()
    p.desapilar()
    igual(p.minimo(), 5)
    igual(p.tope(), 5)


# ---------------------------------------------------- E. búsqueda binaria
@prueba(15, "raiz_entera")
def _(m):
    for n, esperado in [(0, 0), (1, 1), (8, 2), (16, 4), (99, 9), (2147395599, 46339)]:
        igual(m.raiz_entera(n), esperado)


@prueba(16, "buscar_en_rotado")
def _(m):
    igual(m.buscar_en_rotado([4, 5, 6, 7, 0, 1, 2], 0), 4)
    igual(m.buscar_en_rotado([4, 5, 6, 7, 0, 1, 2], 3), -1)
    igual(m.buscar_en_rotado([1], 0), -1)
    igual(m.buscar_en_rotado([3, 1], 1), 1)
    igual(m.buscar_en_rotado([5, 1, 3], 5), 0)


# ------------------------------------------------------ F. listas enlazadas
@prueba(17, "invertir_lista")
def _(m):
    igual(lista_a_python(m.invertir_lista(crear_lista([1, 2, 3, 4]))), [4, 3, 2, 1])
    igual(lista_a_python(m.invertir_lista(crear_lista([1]))), [1])
    igual(m.invertir_lista(None), None)


@prueba(18, "tiene_ciclo")
def _(m):
    cabeza = crear_lista([3, 2, 0, -4])
    cabeza.siguiente.siguiente.siguiente.siguiente = cabeza.siguiente     # -4 apunta a 2
    igual(m.tiene_ciclo(cabeza), True)
    igual(m.tiene_ciclo(crear_lista([1, 2, 3])), False)
    igual(m.tiene_ciclo(None), False)


# ------------------------------------------------------------- G. árboles
@prueba(19, "altura_arbol")
def _(m):
    igual(m.altura_arbol(crear_arbol([3, 9, 20, None, None, 15, 7])), 3)
    igual(m.altura_arbol(crear_arbol([1, None, 2])), 2)
    igual(m.altura_arbol(None), 0)


@prueba(20, "recorrido_por_niveles")
def _(m):
    igual(m.recorrido_por_niveles(crear_arbol([3, 9, 20, None, None, 15, 7])), [[3], [9, 20], [15, 7]])
    igual(m.recorrido_por_niveles(crear_arbol([1])), [[1]])
    igual(m.recorrido_por_niveles(None), [])


@prueba(21, "es_bst_valido")
def _(m):
    igual(m.es_bst_valido(crear_arbol([2, 1, 3])), True)
    igual(m.es_bst_valido(crear_arbol([5, 1, 4, None, None, 3, 6])), False)
    igual(m.es_bst_valido(crear_arbol([5, 4, 6, None, None, 3, 7])), False)   # 3 < 5 en el lado derecho
    igual(m.es_bst_valido(None), True)


# --------------------------------------------------------------- H. grafos
@prueba(22, "contar_islas")
def _(m):
    mapa = ["11000",
            "11000",
            "00100",
            "00011"]
    igual(m.contar_islas(mapa), 3)
    igual(m.contar_islas(["111", "010", "111"]), 1)
    igual(m.contar_islas(["000"]), 0)


@prueba(23, "orden_cursos")
def _(m):
    def es_valido(orden, n, prerrequisitos):
        posicion = {materia: i for i, materia in enumerate(orden)}
        return (sorted(orden) == list(range(n))
                and all(posicion[req] < posicion[mat] for mat, req in prerrequisitos))

    pre = [[1, 0], [2, 0], [3, 1], [3, 2]]
    orden = m.orden_cursos(4, pre)
    if not es_valido(orden, 4, pre):
        raise AssertionError(f"orden no válido: {orden!r}")
    igual(m.orden_cursos(2, [[1, 0], [0, 1]]), [])           # ciclo
    igual(sorted(m.orden_cursos(3, [])), [0, 1, 2])


# --------------------------------------------------------- I. backtracking
@prueba(24, "subconjuntos")
def _(m):
    igual(normalizar(m.subconjuntos([1, 2, 3])),
          normalizar([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]))
    igual(m.subconjuntos([]), [[]])


@prueba(25, "permutaciones")
def _(m):
    obtenido = m.permutaciones([1, 2, 3])
    igual(sorted(obtenido), [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]])
    igual(m.permutaciones([1]), [[1]])


# ------------------------------------------------ J. programación dinámica
@prueba(26, "formas_subir_escalera")
def _(m):
    for n, esperado in [(1, 1), (2, 2), (3, 3), (5, 8), (45, 1836311903)]:
        igual(m.formas_subir_escalera(n), esperado)


@prueba(27, "max_subarreglo")
def _(m):
    igual(m.max_subarreglo([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)
    igual(m.max_subarreglo([-3, -1, -2]), -1)
    igual(m.max_subarreglo([5]), 5)


@prueba(28, "subsecuencia_comun_mas_larga")
def _(m):
    igual(m.subsecuencia_comun_mas_larga("abcde", "ace"), 3)
    igual(m.subsecuencia_comun_mas_larga("abc", "abc"), 3)
    igual(m.subsecuencia_comun_mas_larga("abc", "def"), 0)


# ------------------------------------------------ K. ordenamiento y diseño
@prueba(29, "merge_sort")
def _(m):
    original = [5, 2, 9, 1, 5, 6]
    igual(m.merge_sort(original), [1, 2, 5, 5, 6, 9])
    igual(original, [5, 2, 9, 1, 5, 6])                     # no debe modificar la entrada
    igual(m.merge_sort([]), [])


@prueba(30, "CacheLRU")
def _(m):
    c = m.CacheLRU(2)
    c.poner(1, 1)
    c.poner(2, 2)
    igual(c.obtener(1), 1)
    c.poner(3, 3)               # expulsa la clave 2 (la usada hace más tiempo)
    igual(c.obtener(2), -1)
    c.poner(4, 4)               # expulsa la clave 1
    igual(c.obtener(1), -1)
    igual(c.obtener(3), 3)
    igual(c.obtener(4), 4)


# ----------------------------------------------------------------- runner
def main():
    nombre_modulo = sys.argv[1].removesuffix(".py") if len(sys.argv) > 1 else "soluciones"
    solo = {int(x) for x in sys.argv[2:]}
    modulo = importlib.import_module(nombre_modulo)
    conteo = {"OK": 0, "FALLO": 0, "PENDIENTE": 0}
    print(f"Probando {nombre_modulo}.py\n")
    for numero, nombre, funcion in PRUEBAS:
        if solo and numero not in solo:
            continue
        if not hasattr(modulo, nombre):
            estado, detalle = "PENDIENTE", f"(no existe {nombre} en el archivo)"
        else:
            try:
                funcion(modulo)
                estado, detalle = "OK", ""
            except NotImplementedError:
                estado, detalle = "PENDIENTE", ""
            except Exception as e:  # noqa: BLE001 — mostrar cualquier error de la solución
                estado, detalle = "FALLO", f"{type(e).__name__}: {e}"
        conteo[estado] += 1
        print(f"{numero:>2}. {nombre:<34} {estado:<9} {detalle}")
    total = sum(conteo.values())
    print(f"\n{conteo['OK']}/{total} correctas | {conteo['FALLO']} con fallos | {conteo['PENDIENTE']} pendientes")
    sys.exit(0 if conteo["OK"] == total else 1)


if __name__ == "__main__":
    main()
