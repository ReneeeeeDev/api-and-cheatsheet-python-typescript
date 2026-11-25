"""Plantilla para practicar los 30 problemas de PROBLEMAS.md.

1. Copia este archivo:      copy plantilla.py mis_soluciones.py     (Linux/Mac: cp)
2. Resuelve un problema reemplazando `raise NotImplementedError`.
3. Prueba:                  python pruebas.py mis_soluciones 1      (o sin número para todos)

Cronométrate: ⭐ 10 min · ⭐⭐ 20 min · ⭐⭐⭐ 30 min. Di en voz alta lo que piensas.
Las listas enlazadas y árboles usan las clases de estructuras.py (.valor, .siguiente, .izq, .der).
"""


# ======================================================== A. ARREGLOS Y HASH
def contiene_duplicado(nums):
    """1. ¿Algún valor aparece dos veces? [1, 2, 3, 1] → True"""
    raise NotImplementedError


def elemento_mayoritario(nums):
    """2. El valor que aparece más de n/2 veces (siempre existe). [2, 2, 1, 1, 1, 2, 2] → 2"""
    raise NotImplementedError


def secuencia_consecutiva_mas_larga(nums):
    """3. Largo de la mayor secuencia de enteros consecutivos, en O(n). [100, 4, 200, 1, 3, 2] → 4"""
    raise NotImplementedError


def subarreglos_suma_k(nums, k):
    """4. Cuántos subarreglos contiguos suman k (puede haber negativos). [1, 1, 1], 2 → 2"""
    raise NotImplementedError


def producto_excepto_si_mismo(nums):
    """5. resultado[i] = producto de todos menos nums[i], SIN división. [1, 2, 3, 4] → [24, 12, 8, 6]"""
    raise NotImplementedError


# ============================================================ B. DOS PUNTEROS
def mover_ceros(nums):
    """6. Mover los ceros al final EN LA MISMA lista, conservando el orden del resto.
    [0, 1, 0, 3, 12] → [1, 3, 12, 0, 0]"""
    raise NotImplementedError


def fusionar_ordenadas(a, b):
    """7. Unir dos listas ordenadas en una ordenada, sin sort(). [1, 3, 5], [2, 4] → [1, 2, 3, 4, 5]"""
    raise NotImplementedError


def tres_suma(nums):
    """8. Todas las tripletas distintas que suman 0. [-1, 0, 1, 2, -1, -4] → [[-1, -1, 2], [-1, 0, 1]]"""
    raise NotImplementedError


def contenedor_mas_agua(alturas):
    """9. Área máxima entre dos líneas: (j - i) * min(h[i], h[j]). [1, 8, 6, 2, 5, 4, 8, 3, 7] → 49"""
    raise NotImplementedError


# ======================================================= C. VENTANA DESLIZANTE
def max_suma_ventana(nums, k):
    """10. Mayor suma de k elementos seguidos; None si k no es válido. [2, 1, 5, 1, 3, 2], 3 → 9"""
    raise NotImplementedError


def subcadena_sin_repetir(s):
    """11. Largo de la subcadena más larga sin letras repetidas. "abcabcbb" → 3"""
    raise NotImplementedError


# =================================================================== D. PILAS
def evaluar_rpn(tokens):
    """12. Evaluar notación polaca inversa; la división trunca hacia 0.
    ["2", "1", "+", "3", "*"] → 9"""
    raise NotImplementedError


def temperaturas_diarias(temps):
    """13. Para cada día, cuántos días esperar hasta uno más cálido (0 si no hay).
    [73, 74, 75, 71, 69, 72, 76, 73] → [1, 1, 4, 2, 1, 1, 0, 0]"""
    raise NotImplementedError


class PilaMinima:
    """14. Pila con apilar, desapilar, tope y minimo, todas en O(1)."""

    def __init__(self):
        raise NotImplementedError

    def apilar(self, x):
        raise NotImplementedError

    def desapilar(self):
        raise NotImplementedError

    def tope(self):
        raise NotImplementedError

    def minimo(self):
        raise NotImplementedError


# ======================================================== E. BÚSQUEDA BINARIA
def raiz_entera(n):
    """15. Parte entera de √n sin math.sqrt ni ** 0.5. 8 → 2"""
    raise NotImplementedError


def buscar_en_rotado(nums, objetivo):
    """16. Índice del objetivo en una lista ordenada y rotada, en O(log n). [4, 5, 6, 7, 0, 1, 2], 0 → 4"""
    raise NotImplementedError


# ======================================================= F. LISTAS ENLAZADAS
def invertir_lista(cabeza):
    """17. Invertir la lista enlazada y devolver la nueva cabeza. 1->2->3 → 3->2->1"""
    raise NotImplementedError


def tiene_ciclo(cabeza):
    """18. ¿La lista enlazada tiene un ciclo? Con O(1) de memoria extra."""
    raise NotImplementedError


# ================================================================= G. ÁRBOLES
def altura_arbol(raiz):
    """19. Número de niveles del árbol (None → 0)."""
    raise NotImplementedError


def recorrido_por_niveles(raiz):
    """20. Valores agrupados por nivel. [3, 9, 20, None, None, 15, 7] → [[3], [9, 20], [15, 7]]"""
    raise NotImplementedError


def es_bst_valido(raiz):
    """21. ¿Es un árbol binario de búsqueda (izq < nodo < der en TODO el subárbol)?"""
    raise NotImplementedError


# ================================================================== H. GRAFOS
def contar_islas(mapa):
    """22. Grupos de "1" conectados en horizontal/vertical. ["110", "010", "001"] → 2"""
    raise NotImplementedError


def orden_cursos(n, prerrequisitos):
    """23. Orden para tomar las materias 0..n-1; [materia, requisito]. [] si es imposible (ciclo)."""
    raise NotImplementedError


# ============================================================ I. BACKTRACKING
def subconjuntos(nums):
    """24. Todos los subconjuntos. [1, 2] → [[], [1], [2], [1, 2]] (en cualquier orden)"""
    raise NotImplementedError


def permutaciones(nums):
    """25. Todas las permutaciones (valores distintos). [1, 2] → [[1, 2], [2, 1]]"""
    raise NotImplementedError


# ================================================ J. PROGRAMACIÓN DINÁMICA
def formas_subir_escalera(n):
    """26. Formas de subir n escalones de 1 en 1 o de 2 en 2. 5 → 8"""
    raise NotImplementedError


def max_subarreglo(nums):
    """27. Mayor suma de un subarreglo contiguo. [-2, 1, -3, 4, -1, 2, 1, -5, 4] → 6"""
    raise NotImplementedError


def subsecuencia_comun_mas_larga(a, b):
    """28. Largo de la subsecuencia común más larga. "abcde", "ace" → 3"""
    raise NotImplementedError


# ================================================ K. ORDENAMIENTO Y DISEÑO
def merge_sort(lista):
    """29. Ordenar con merge sort, sin modificar la lista original."""
    raise NotImplementedError


class CacheLRU:
    """30. Caché con capacidad fija; al llenarse expulsa la clave usada hace más tiempo.
    obtener(clave) → valor o -1; poner(clave, valor). Ambas en O(1)."""

    def __init__(self, capacidad):
        raise NotImplementedError

    def obtener(self, clave):
        raise NotImplementedError

    def poner(self, clave, valor):
        raise NotImplementedError
