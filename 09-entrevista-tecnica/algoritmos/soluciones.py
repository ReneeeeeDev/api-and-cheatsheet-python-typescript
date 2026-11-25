"""Soluciones de referencia de los 30 problemas de entrevista (PROBLEMAS.md).

Cada función dice qué patrón usa y su complejidad. Comprobarlas: python pruebas.py
Intenta cada problema en mis_soluciones.py ANTES de leer esto.
"""
from collections import OrderedDict, deque


# ======================================================== A. ARREGLOS Y HASH
def contiene_duplicado(nums):
    """1. Set de vistos. O(n) tiempo, O(n) espacio."""
    vistos = set()
    for n in nums:
        if n in vistos:
            return True
        vistos.add(n)
    return False


def elemento_mayoritario(nums):
    """2. Boyer-Moore: el mayoritario 'sobrevive' a las cancelaciones. O(n), O(1) espacio."""
    candidato, votos = None, 0
    for n in nums:
        if votos == 0:
            candidato = n
        votos += 1 if n == candidato else -1
    return candidato


def secuencia_consecutiva_mas_larga(nums):
    """3. Set + contar solo desde el inicio de cada secuencia (n - 1 no está). O(n)."""
    conjunto = set(nums)
    mejor = 0
    for n in conjunto:
        if n - 1 not in conjunto:
            largo = 1
            while n + largo in conjunto:
                largo += 1
            mejor = max(mejor, largo)
    return mejor


def subarreglos_suma_k(nums, k):
    """4. Sumas prefijas + diccionario: si (prefijo - k) ya apareció, entre ese punto
    y el actual hay un subarreglo que suma k. O(n). Funciona con negativos."""
    conteo = {0: 1}
    prefijo = total = 0
    for n in nums:
        prefijo += n
        total += conteo.get(prefijo - k, 0)
        conteo[prefijo] = conteo.get(prefijo, 0) + 1
    return total


def producto_excepto_si_mismo(nums):
    """5. Dos pasadas: producto de todo lo de la izquierda × todo lo de la derecha.
    Sin división (así no falla con ceros). O(n)."""
    resultado = [1] * len(nums)
    izquierda = 1
    for i in range(len(nums)):
        resultado[i] = izquierda
        izquierda *= nums[i]
    derecha = 1
    for i in range(len(nums) - 1, -1, -1):
        resultado[i] *= derecha
        derecha *= nums[i]
    return resultado


# ============================================================ B. DOS PUNTEROS
def mover_ceros(nums):
    """6. Puntero de escritura y puntero de lectura en el mismo arreglo. O(n), O(1) espacio."""
    escribir = 0
    for leer in range(len(nums)):
        if nums[leer] != 0:
            nums[escribir], nums[leer] = nums[leer], nums[escribir]
            escribir += 1
    return nums


def fusionar_ordenadas(a, b):
    """7. Un puntero por lista; siempre se toma el menor. O(n + m). Es el 'merge' de merge sort."""
    i = j = 0
    resultado = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            resultado.append(a[i])
            i += 1
        else:
            resultado.append(b[j])
            j += 1
    resultado.extend(a[i:])
    resultado.extend(b[j:])
    return resultado


def tres_suma(nums):
    """8. Ordenar + fijar uno + dos punteros para los otros dos. O(n²).
    Saltar valores repetidos evita tripletas duplicadas."""
    nums = sorted(nums)
    resultado = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        izq, der = i + 1, len(nums) - 1
        while izq < der:
            suma = nums[i] + nums[izq] + nums[der]
            if suma < 0:
                izq += 1
            elif suma > 0:
                der -= 1
            else:
                resultado.append([nums[i], nums[izq], nums[der]])
                izq += 1
                der -= 1
                while izq < der and nums[izq] == nums[izq - 1]:
                    izq += 1
    return resultado


def contenedor_mas_agua(alturas):
    """9. Punteros en los extremos; mover el lado más bajo (el alto nunca mejora el área). O(n)."""
    izq, der = 0, len(alturas) - 1
    mejor = 0
    while izq < der:
        mejor = max(mejor, (der - izq) * min(alturas[izq], alturas[der]))
        if alturas[izq] < alturas[der]:
            izq += 1
        else:
            der -= 1
    return mejor


# ======================================================= C. VENTANA DESLIZANTE
def max_suma_ventana(nums, k):
    """10. Ventana fija: sumar el que entra y restar el que sale. O(n)."""
    if k <= 0 or k > len(nums):
        return None
    ventana = sum(nums[:k])
    mejor = ventana
    for i in range(k, len(nums)):
        ventana += nums[i] - nums[i - k]
        mejor = max(mejor, ventana)
    return mejor


def subcadena_sin_repetir(s):
    """11. Ventana variable: si la letra ya está dentro de la ventana, el inicio
    salta a la posición siguiente a su última aparición. O(n)."""
    ultima = {}
    inicio = mejor = 0
    for i, c in enumerate(s):
        if c in ultima and ultima[c] >= inicio:
            inicio = ultima[c] + 1
        ultima[c] = i
        mejor = max(mejor, i - inicio + 1)
    return mejor


# =================================================================== D. PILAS
def evaluar_rpn(tokens):
    """12. Pila: los números se apilan; un operador saca dos y apila el resultado. O(n)."""
    pila = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = pila.pop()          # ¡el orden importa!: b sale primero
            a = pila.pop()
            if t == "+":
                pila.append(a + b)
            elif t == "-":
                pila.append(a - b)
            elif t == "*":
                pila.append(a * b)
            else:
                pila.append(int(a / b))     # trunca hacia 0 (// redondea hacia -∞)
        else:
            pila.append(int(t))
    return pila[0]


def temperaturas_diarias(temps):
    """13. Pila monótona con los índices de los días que aún esperan un día más cálido. O(n)."""
    respuesta = [0] * len(temps)
    pila = []
    for i, t in enumerate(temps):
        while pila and temps[pila[-1]] < t:
            j = pila.pop()
            respuesta[j] = i - j
        pila.append(i)
    return respuesta


class PilaMinima:
    """14. Cada elemento guarda también el mínimo hasta ese punto: todo en O(1)."""

    def __init__(self):
        self._datos = []            # pares (valor, mínimo hasta aquí)

    def apilar(self, x):
        minimo = x if not self._datos else min(x, self._datos[-1][1])
        self._datos.append((x, minimo))

    def desapilar(self):
        return self._datos.pop()[0]

    def tope(self):
        return self._datos[-1][0]

    def minimo(self):
        return self._datos[-1][1]


# ======================================================== E. BÚSQUEDA BINARIA
def raiz_entera(n):
    """15. Búsqueda binaria sobre la respuesta: el mayor r con r*r <= n. O(log n)."""
    izq, der = 0, n
    while izq <= der:
        medio = (izq + der) // 2
        if medio * medio <= n:
            izq = medio + 1
        else:
            der = medio - 1
    return der


def buscar_en_rotado(nums, objetivo):
    """16. En cada paso al menos una mitad está ordenada; ver si el objetivo cae en ella. O(log n)."""
    izq, der = 0, len(nums) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if nums[medio] == objetivo:
            return medio
        if nums[izq] <= nums[medio]:                # mitad izquierda ordenada
            if nums[izq] <= objetivo < nums[medio]:
                der = medio - 1
            else:
                izq = medio + 1
        else:                                       # mitad derecha ordenada
            if nums[medio] < objetivo <= nums[der]:
                izq = medio + 1
            else:
                der = medio - 1
    return -1


# ======================================================= F. LISTAS ENLAZADAS
def invertir_lista(cabeza):
    """17. Tres punteros: anterior, actual, siguiente. O(n), O(1) espacio."""
    anterior = None
    actual = cabeza
    while actual is not None:
        siguiente = actual.siguiente
        actual.siguiente = anterior
        anterior = actual
        actual = siguiente
    return anterior


def tiene_ciclo(cabeza):
    """18. Floyd (tortuga y liebre): si hay ciclo, el rápido alcanza al lento. O(n), O(1) espacio."""
    lento = rapido = cabeza
    while rapido is not None and rapido.siguiente is not None:
        lento = lento.siguiente
        rapido = rapido.siguiente.siguiente
        if lento is rapido:
            return True
    return False


# ================================================================= G. ÁRBOLES
def altura_arbol(raiz):
    """19. Recursión (DFS): 1 + la altura del subárbol más alto. O(n)."""
    if raiz is None:
        return 0
    return 1 + max(altura_arbol(raiz.izq), altura_arbol(raiz.der))


def recorrido_por_niveles(raiz):
    """20. BFS con cola; en cada vuelta se procesa un nivel completo. O(n)."""
    if raiz is None:
        return []
    niveles = []
    cola = deque([raiz])
    while cola:
        nivel = []
        for _ in range(len(cola)):
            nodo = cola.popleft()
            nivel.append(nodo.valor)
            if nodo.izq:
                cola.append(nodo.izq)
            if nodo.der:
                cola.append(nodo.der)
        niveles.append(nivel)
    return niveles


def es_bst_valido(raiz, minimo=None, maximo=None):
    """21. Cada nodo debe estar dentro del rango (minimo, maximo) que heredan sus
    ancestros; comparar solo con el padre NO basta. O(n)."""
    if raiz is None:
        return True
    if minimo is not None and raiz.valor <= minimo:
        return False
    if maximo is not None and raiz.valor >= maximo:
        return False
    return (es_bst_valido(raiz.izq, minimo, raiz.valor)
            and es_bst_valido(raiz.der, raiz.valor, maximo))


# ================================================================== H. GRAFOS
def contar_islas(mapa):
    """22. Cada '1' sin visitar inicia un BFS que marca toda su isla. O(filas × columnas).
    No modifica la entrada (usa un set de visitados)."""
    if not mapa:
        return 0
    filas, columnas = len(mapa), len(mapa[0])
    visitados = set()
    islas = 0
    for f in range(filas):
        for c in range(columnas):
            if mapa[f][c] != "1" or (f, c) in visitados:
                continue
            islas += 1
            visitados.add((f, c))
            cola = deque([(f, c)])
            while cola:
                x, y = cola.popleft()
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if (0 <= nx < filas and 0 <= ny < columnas
                            and mapa[nx][ny] == "1" and (nx, ny) not in visitados):
                        visitados.add((nx, ny))
                        cola.append((nx, ny))
    return islas


def orden_cursos(n, prerrequisitos):
    """23. Orden topológico (Kahn): tomar primero las materias sin requisitos pendientes.
    Si al final no se tomaron todas, hay un ciclo → []. O(V + E)."""
    siguientes = [[] for _ in range(n)]
    pendientes = [0] * n
    for materia, requisito in prerrequisitos:
        siguientes[requisito].append(materia)
        pendientes[materia] += 1
    cola = deque(i for i in range(n) if pendientes[i] == 0)
    orden = []
    while cola:
        actual = cola.popleft()
        orden.append(actual)
        for materia in siguientes[actual]:
            pendientes[materia] -= 1
            if pendientes[materia] == 0:
                cola.append(materia)
    return orden if len(orden) == n else []


# ============================================================ I. BACKTRACKING
def subconjuntos(nums):
    """24. Para cada elemento: lo tomo / no lo tomo. O(n · 2ⁿ)."""
    resultado = []
    actual = []

    def explorar(i):
        if i == len(nums):
            resultado.append(actual.copy())
            return
        actual.append(nums[i])      # lo tomo
        explorar(i + 1)
        actual.pop()                # deshago la decisión
        explorar(i + 1)             # no lo tomo

    explorar(0)
    return resultado


def permutaciones(nums):
    """25. Elegir uno de los que quedan, recursión, deshacer. O(n · n!)."""
    resultado = []
    actual = []
    usados = [False] * len(nums)

    def explorar():
        if len(actual) == len(nums):
            resultado.append(actual.copy())
            return
        for i, n in enumerate(nums):
            if not usados[i]:
                usados[i] = True
                actual.append(n)
                explorar()
                actual.pop()
                usados[i] = False

    explorar()
    return resultado


# ================================================ J. PROGRAMACIÓN DINÁMICA
def formas_subir_escalera(n):
    """26. formas(n) = formas(n-1) + formas(n-2): es Fibonacci. O(n) tiempo, O(1) espacio."""
    anterior, actual = 1, 1         # formas(0), formas(1)
    for _ in range(n - 1):
        anterior, actual = actual, anterior + actual
    return actual


def max_subarreglo(nums):
    """27. Kadane: en cada posición, ¿sigo la racha o empiezo de nuevo aquí? O(n)."""
    mejor = actual = nums[0]
    for n in nums[1:]:
        actual = max(n, actual + n)
        mejor = max(mejor, actual)
    return mejor


def subsecuencia_comun_mas_larga(a, b):
    """28. Tabla dp[i][j] = LCS de a[:i] y b[:j]. O(len(a) × len(b))."""
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


# ================================================ K. ORDENAMIENTO Y DISEÑO
def merge_sort(lista):
    """29. Divide y vencerás: ordenar cada mitad y fusionarlas (problema 7).
    O(n log n) siempre, estable, no modifica la entrada."""
    if len(lista) <= 1:
        return list(lista)
    medio = len(lista) // 2
    return fusionar_ordenadas(merge_sort(lista[:medio]), merge_sort(lista[medio:]))


class CacheLRU:
    """30. OrderedDict recuerda el orden de uso: al usar una clave se mueve al final
    y se expulsa la del inicio (la usada hace más tiempo). obtener y poner en O(1).
    Sin OrderedDict: diccionario + lista doblemente enlazada."""

    def __init__(self, capacidad):
        self.capacidad = capacidad
        self._datos = OrderedDict()

    def obtener(self, clave):
        if clave not in self._datos:
            return -1
        self._datos.move_to_end(clave)
        return self._datos[clave]

    def poner(self, clave, valor):
        if clave in self._datos:
            self._datos.move_to_end(clave)
        self._datos[clave] = valor
        if len(self._datos) > self.capacidad:
            self._datos.popitem(last=False)
