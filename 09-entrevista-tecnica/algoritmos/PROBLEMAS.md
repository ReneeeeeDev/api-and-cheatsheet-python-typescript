# 30 problemas clásicos de entrevista técnica (por patrón)

Son los problemas que más se repiten en entrevistas de *live coding*, agrupados por **patrón**. En la entrevista no te evalúan por memorizar soluciones: te evalúan por **reconocer el patrón** y explicarlo. Los 50 ejercicios de `03-logica/` son el calentamiento; aquí está el siguiente nivel.

## Cómo practicar

```bash
cd 09-entrevista-tecnica/algoritmos
copy plantilla.py mis_soluciones.py          # o: copy plantilla.js mis_soluciones.js
python pruebas.py mis_soluciones 1           # prueba solo el problema 1
python pruebas.py mis_soluciones             # todos: OK / FALLO / PENDIENTE
node pruebas.js mis_soluciones.js 1          # lo mismo en JavaScript
```

1. Lee el enunciado y **cronométrate**: ⭐ 10 min, ⭐⭐ 20 min, ⭐⭐⭐ 30 min.
2. Antes de programar, di en voz alta (o escribe en un comentario) la idea y su complejidad. Sigue el método de [01-METODO-LIVE-CODING.md](../01-METODO-LIVE-CODING.md).
3. Si a la mitad del tiempo no avanzas, abre la **pista**. Si se acaba el tiempo, lee la solución en `soluciones.py` / `soluciones.js`, **ciérrala** y vuelve a escribirla tú al día siguiente.
4. Anota tu resultado en la tabla de seguimiento del [plan de estudio](../02-PLAN-DE-ESTUDIO.md).

> Las soluciones de referencia pasan las pruebas en los dos lenguajes (30/30). Cada función dice el patrón y la complejidad en su comentario.

| Patrón | Problemas | Señal en el enunciado |
|---|---|---|
| A. Hash (dict / Set / Map) | 1–5 | "¿existe?", "contar", "pares que suman", "en O(n)" |
| B. Dos punteros | 6–9 | Arreglo **ordenado**, "en el mismo arreglo", "pares/tripletas" |
| C. Ventana deslizante | 10–11 | "subarreglo/subcadena **contigua** más larga/corta" |
| D. Pila | 12–13 (y 14) | Paréntesis, expresiones, "el siguiente mayor", deshacer |
| E. Búsqueda binaria | 15–16 | Ordenado, "en O(log n)", "el mínimo valor que cumple…" |
| F. Listas enlazadas | 17–18 | Punteros, "en O(1) de memoria" |
| G. Árboles | 19–21 | Recursión (DFS) o por niveles (BFS) |
| H. Grafos | 22–23 | Cuadrículas, dependencias, "conectados", "orden" |
| I. Backtracking | 24–25 | "**todas** las combinaciones/permutaciones" |
| J. Programación dinámica | 26–28 | "¿de cuántas formas…?", "máximo/mínimo" con decisiones que se repiten |
| K. Ordenamiento y diseño | 29–30 | "implementa…", "diseña una clase…" |

---

## A. Arreglos y hash

### 1. Contiene duplicado — ⭐
Devuelve `True` si algún valor aparece al menos dos veces. `[1, 2, 3, 1]` → `True`; `[1, 2, 3, 4]` → `False`.
**Objetivo:** O(n) tiempo.

<details><summary>Pista</summary>Recorre una vez guardando lo que ya viste en un <code>set</code>. Alternativa en una línea: comparar <code>len(set(nums))</code> con <code>len(nums)</code>. Menciona también la opción de ordenar: O(n log n) pero O(1) de memoria.</details>

### 2. Elemento mayoritario — ⭐
Devuelve el valor que aparece **más de n/2 veces** (siempre existe). `[2, 2, 1, 1, 1, 2, 2]` → `2`.
**Objetivo:** O(n) tiempo; extra: O(1) de memoria.

<details><summary>Pista</summary>Con un diccionario de conteos es O(n) y O(n) de memoria. Para O(1): algoritmo de votación de Boyer-Moore. Guarda un candidato y un contador; si el contador llega a 0 cambias de candidato; +1 si coincide, −1 si no.</details>

### 3. Secuencia consecutiva más larga — ⭐⭐
Largo de la secuencia más larga de enteros consecutivos (en cualquier orden). `[100, 4, 200, 1, 3, 2]` → `4` (1, 2, 3, 4).
**Objetivo:** O(n), es decir, **sin ordenar**.

<details><summary>Pista</summary>Mete todo en un <code>set</code>. Un número <code>n</code> es el inicio de una secuencia solo si <code>n - 1</code> NO está en el set; desde ahí cuenta hacia arriba. Cada número se visita como mucho dos veces.</details>

### 4. Subarreglos que suman k — ⭐⭐
¿Cuántos subarreglos **contiguos** suman exactamente `k`? Puede haber negativos. `[1, 1, 1], k=2` → `2`; `[1, -1, 0], k=0` → `3`.
**Objetivo:** O(n).

<details><summary>Pista</summary>Sumas prefijas. Si la suma acumulada hasta i es <code>P</code> y antes hubo una suma acumulada <code>P - k</code>, el tramo entre ambas suma k. Guarda en un diccionario cuántas veces apareció cada suma acumulada (empieza con <code>{0: 1}</code>). La ventana deslizante no sirve aquí porque hay negativos.</details>

### 5. Producto de todos excepto sí mismo — ⭐⭐
`resultado[i]` = producto de todos los elementos menos `nums[i]`, **sin usar división**. `[1, 2, 3, 4]` → `[24, 12, 8, 6]`.
**Objetivo:** O(n).

<details><summary>Pista</summary>Cada resultado = (producto de todo lo que está a la izquierda) × (producto de todo lo que está a la derecha). Una pasada de izquierda a derecha y otra de derecha a izquierda. Pregunta al entrevistador por los ceros: es la razón por la que no se usa división.</details>

---

## B. Dos punteros

### 6. Mover ceros — ⭐
Mueve los ceros al final **modificando la misma lista** y conservando el orden del resto. `[0, 1, 0, 3, 12]` → `[1, 3, 12, 0, 0]`.
**Objetivo:** O(n) tiempo, O(1) memoria.

<details><summary>Pista</summary>Un puntero <code>escribir</code> marca dónde va el próximo número distinto de cero; otro puntero <code>leer</code> recorre todo. Cuando <code>leer</code> encuentra un no-cero, intercambias y avanzas <code>escribir</code>.</details>

### 7. Fusionar dos listas ordenadas — ⭐
`[1, 3, 5]` y `[2, 4]` → `[1, 2, 3, 4, 5]`, **sin** `sort()`.
**Objetivo:** O(n + m).

<details><summary>Pista</summary>Un índice en cada lista; agrega siempre el menor de los dos y avanza ese índice. Al final copia lo que sobre. Es el corazón de merge sort (problema 29).</details>

### 8. Tres suma (3Sum) — ⭐⭐
Todas las tripletas **distintas** que suman 0. `[-1, 0, 1, 2, -1, -4]` → `[[-1, -1, 2], [-1, 0, 1]]`.
**Objetivo:** O(n²).

<details><summary>Pista</summary>Ordena. Fija el primer número <code>i</code> y busca los otros dos con dos punteros (<code>izq = i + 1</code>, <code>der = final</code>): si la suma es menor que 0, mueve <code>izq</code>; si es mayor, mueve <code>der</code>. Salta los valores repetidos para no duplicar tripletas. En JS: <code>sort((a, b) => a - b)</code>.</details>

### 9. Contenedor con más agua — ⭐⭐
`alturas[i]` es la altura de una línea vertical. Elige dos líneas que, junto con el eje X, formen el recipiente con más agua: área = `(j - i) × min(h[i], h[j])`. `[1, 8, 6, 2, 5, 4, 8, 3, 7]` → `49`.
**Objetivo:** O(n).

<details><summary>Pista</summary>Empieza con un puntero en cada extremo (máximo ancho). Mueve siempre el lado <b>más bajo</b>: mover el alto nunca puede mejorar el área, porque el ancho baja y la altura sigue limitada por el bajo.</details>

---

## C. Ventana deslizante

### 10. Máxima suma de k elementos seguidos — ⭐
`[2, 1, 5, 1, 3, 2], k=3` → `9` (5 + 1 + 3). Si `k` no es válido, devuelve `None` / `null`.
**Objetivo:** O(n), sin volver a sumar la ventana completa en cada paso.

<details><summary>Pista</summary>Suma los primeros k. Luego, en cada paso, suma el elemento que entra y resta el que sale (<code>nums[i - k]</code>).</details>

### 11. Subcadena más larga sin repetir letras — ⭐⭐
`"abcabcbb"` → `3` ("abc"); `"bbbbb"` → `1`; `"pwwkew"` → `3` ("wke").
**Objetivo:** O(n).

<details><summary>Pista</summary>Ventana <code>[inicio, i]</code> que nunca tiene repetidos. Guarda en un diccionario la última posición de cada letra. Si la letra actual ya está <b>dentro</b> de la ventana (posición ≥ inicio), mueve <code>inicio</code> a esa posición + 1. Prueba con "abba": es el caso que rompe la mayoría de primeras versiones.</details>

---

## D. Pilas

### 12. Evaluar notación polaca inversa — ⭐⭐
`["2", "1", "+", "3", "*"]` → `9`, porque es `(2 + 1) * 3`. La división **trunca hacia cero**.
**Objetivo:** O(n).

<details><summary>Pista</summary>Números a la pila. Con un operador, saca <code>b</code> y luego <code>a</code> (¡en ese orden!) y apila <code>a op b</code>. En Python, <code>int(a / b)</code> trunca hacia 0; <code>a // b</code> redondea hacia −∞ y falla con negativos.</details>

### 13. Temperaturas diarias — ⭐⭐
Para cada día, ¿cuántos días hay que esperar hasta uno más cálido? 0 si no hay. `[73, 74, 75, 71, 69, 72, 76, 73]` → `[1, 1, 4, 2, 1, 1, 0, 0]`.
**Objetivo:** O(n). La versión de dos bucles es O(n²).

<details><summary>Pista</summary>Pila monótona: guarda los <b>índices</b> de los días que todavía esperan respuesta (sus temperaturas quedan en orden decreciente). Cuando llega un día más cálido que el tope, ese día es la respuesta del tope: lo sacas y calculas la distancia. Repite.</details>

### 14. Pila con mínimo en O(1) — ⭐⭐
Clase `PilaMinima` con `apilar(x)`, `desapilar()`, `tope()` y `minimo()`, **todas en O(1)**.

<details><summary>Pista</summary>Guarda junto a cada valor el mínimo que había hasta ese momento: pares <code>(valor, minimo_hasta_aqui)</code>. Al desapilar, el mínimo anterior "vuelve solo".</details>

---

## E. Búsqueda binaria

### 15. Raíz cuadrada entera — ⭐
Parte entera de √n sin `sqrt` ni `** 0.5`. `8` → `2`; `16` → `4`.
**Objetivo:** O(log n).

<details><summary>Pista</summary>Búsqueda binaria sobre la <b>respuesta</b> entre 0 y n: si <code>medio * medio <= n</code>, la respuesta es ≥ medio (busca a la derecha); si no, a la izquierda. Al terminar, <code>der</code> queda en la respuesta. Este patrón ("el mayor valor que cumple X") aparece mucho.</details>

### 16. Buscar en arreglo ordenado y rotado — ⭐⭐⭐
Una lista ordenada fue rotada: `[4, 5, 6, 7, 0, 1, 2]`. Devuelve el índice del objetivo o −1. Objetivo 0 → `4`.
**Objetivo:** O(log n).

<details><summary>Pista</summary>En cada paso, al menos una mitad está ordenada (compara <code>nums[izq]</code> con <code>nums[medio]</code>). Si el objetivo está dentro del rango de la mitad ordenada, busca ahí; si no, en la otra.</details>

---

## F. Listas enlazadas

Usan las clases de `estructuras.py` / `estructuras.js`: cada nodo tiene `.valor` y `.siguiente`.

### 17. Invertir una lista enlazada — ⭐⭐
`1 → 2 → 3 → 4` → `4 → 3 → 2 → 1`. Devuelve la nueva cabeza.
**Objetivo:** O(n) tiempo, O(1) memoria. Extra: hazlo también recursivo.

<details><summary>Pista</summary>Tres variables: <code>anterior</code> (empieza en None), <code>actual</code> y <code>siguiente</code>. En cada paso: guarda el siguiente, apunta <code>actual.siguiente</code> a <code>anterior</code> y avanza las dos. Dibújalo en papel: es la mejor forma de no perderte.</details>

### 18. Detectar un ciclo — ⭐⭐
¿Algún nodo apunta a uno anterior?
**Objetivo:** O(1) de memoria. Con un set de visitados es fácil, pero usa O(n).

<details><summary>Pista</summary>Floyd, "tortuga y liebre": un puntero avanza de 1 en 1 y otro de 2 en 2. Si hay ciclo, se encuentran; si el rápido llega a None, no hay ciclo.</details>

---

## G. Árboles

Usan `NodoArbol` (`.valor`, `.izq`, `.der`). Las pruebas crean los árboles desde listas por niveles: `[3, 9, 20, None, None, 15, 7]`.

### 19. Altura de un árbol — ⭐
Número de niveles. Árbol vacío → 0.

<details><summary>Pista</summary>Caso base: None → 0. Caso recursivo: 1 + max(altura izquierda, altura derecha). Es la plantilla de casi todos los problemas de árboles.</details>

### 20. Recorrido por niveles — ⭐⭐
`[3, 9, 20, None, None, 15, 7]` → `[[3], [9, 20], [15, 7]]`.

<details><summary>Pista</summary>BFS con una cola (<code>collections.deque</code>). Truco: al empezar cada vuelta, <code>len(cola)</code> es exactamente la cantidad de nodos de ese nivel.</details>

### 21. ¿Es un árbol binario de búsqueda? — ⭐⭐
En un BST, **todo** el subárbol izquierdo es menor que el nodo y **todo** el derecho es mayor.

<details><summary>Pista</summary>Comparar cada nodo solo con sus hijos NO basta: en <code>[5, 4, 6, None, None, 3, 7]</code> el 3 está a la derecha del 5. Pasa en la recursión un rango <code>(minimo, maximo)</code> permitido: al ir a la izquierda el máximo pasa a ser el valor del nodo; al ir a la derecha, el mínimo.</details>

---

## H. Grafos

### 22. Contar islas — ⭐⭐
Cuadrícula de `"1"` (tierra) y `"0"` (agua). Una isla es un grupo de 1 conectados en horizontal o vertical.

```
11000
11000      → 3 islas
00100
00011
```

<details><summary>Pista</summary>Recorre todas las celdas. Cada vez que encuentres un "1" no visitado, suma una isla y lanza un BFS/DFS que marque como visitada toda esa isla. Usa un set de visitados para no modificar la entrada (pregunta si puedes modificarla).</details>

### 23. Orden de materias con prerrequisitos — ⭐⭐⭐
Hay `n` materias (0..n−1) y pares `[materia, requisito]`. Devuelve un orden válido para cursarlas todas, o `[]` si es imposible (hay un ciclo).
`n = 4, [[1, 0], [2, 0], [3, 1], [3, 2]]` → `[0, 1, 2, 3]` (o `[0, 2, 1, 3]`).

<details><summary>Pista</summary>Orden topológico, algoritmo de Kahn. Cuenta cuántos requisitos pendientes tiene cada materia. Mete en una cola las que tienen 0. Al "tomar" una materia, resta 1 a las que dependen de ella; si alguna llega a 0, entra a la cola. Si al final no tomaste las n materias, hay un ciclo.</details>

---

## I. Backtracking

### 24. Subconjuntos — ⭐⭐
Todos los subconjuntos de `[1, 2, 3]` (8, incluido `[]`). En cualquier orden.

<details><summary>Pista</summary>Para cada elemento decides "lo tomo" o "no lo tomo": un árbol de decisiones de profundidad n, con 2ⁿ hojas. Patrón: elegir → explorar → <b>deshacer</b> (<code>append</code> → recursión → <code>pop</code>). Guarda una <b>copia</b> de la lista actual, no la referencia.</details>

### 25. Permutaciones — ⭐⭐
Todas las permutaciones de `[1, 2, 3]` (6).

<details><summary>Pista</summary>Mismo patrón que el 24, pero en cada nivel eliges cualquiera de los elementos que aún no usaste (lleva un arreglo <code>usados</code>). Cuando la lista actual tiene n elementos, guardas una copia.</details>

---

## J. Programación dinámica

### 26. Formas de subir una escalera — ⭐
Puedes subir 1 o 2 escalones a la vez. ¿De cuántas formas subes `n` escalones? `3` → `3` (1+1+1, 1+2, 2+1); `5` → `8`.
**Objetivo:** O(n) y que `n = 45` responda al instante.

<details><summary>Pista</summary>Para llegar al escalón n vienes del n−1 o del n−2: <code>formas(n) = formas(n-1) + formas(n-2)</code>. Es Fibonacci. La recursión directa es O(2ⁿ); con memoización o con dos variables es O(n). Explica esa diferencia: es exactamente lo que quieren escuchar.</details>

### 27. Subarreglo de suma máxima — ⭐⭐
`[-2, 1, -3, 4, -1, 2, 1, -5, 4]` → `6` (el tramo `[4, -1, 2, 1]`).
**Objetivo:** O(n).

<details><summary>Pista</summary>Kadane: <code>actual = max(n, actual + n)</code>. ¿Me conviene seguir con la racha o empezar de nuevo aquí? Guarda el mejor visto. Cuidado: si todos son negativos, la respuesta es el mayor de ellos, no 0.</details>

### 28. Subsecuencia común más larga — ⭐⭐⭐
Largo de la subsecuencia común más larga (no tiene que ser contigua). `"abcde"`, `"ace"` → `3`.
**Objetivo:** O(len(a) × len(b)).

<details><summary>Pista</summary>Tabla <code>dp[i][j]</code> = respuesta para <code>a[:i]</code> y <code>b[:j]</code>. Si <code>a[i-1] == b[j-1]</code>: <code>dp[i-1][j-1] + 1</code>; si no: <code>max(dp[i-1][j], dp[i][j-1])</code>. Dibuja la tabla con "abcde" y "ace" antes de programar. Es la base de <code>diff</code> y de git.</details>

---

## K. Ordenamiento y diseño

### 29. Merge sort — ⭐⭐
Ordena con merge sort **sin modificar** la lista original.

<details><summary>Pista</summary>Si tiene 0 o 1 elementos, ya está ordenada. Si no: parte en dos, ordena cada mitad (recursión) y fusiónalas con el problema 7. Ten lista la comparación: merge sort es O(n log n) siempre y estable, pero usa O(n) de memoria; quicksort es O(n log n) en promedio, O(n²) en el peor caso y ordena en el mismo arreglo.</details>

### 30. Caché LRU — ⭐⭐⭐
Clase `CacheLRU(capacidad)` con `obtener(clave)` (valor o −1) y `poner(clave, valor)`. Al superar la capacidad, expulsa la clave **usada hace más tiempo**. Ambas operaciones en O(1).

<details><summary>Pista</summary>Necesitas búsqueda O(1) (diccionario) y además saber el orden de uso. En Python, <code>OrderedDict</code> con <code>move_to_end</code> y <code>popitem(last=False)</code>. En JS, un <code>Map</code> conserva el orden de inserción: borrar y volver a insertar mueve la clave al final. Si te piden hacerlo "a mano": diccionario + lista doblemente enlazada.</details>

---

**Siguiente nivel:** cuando resuelvas estos 30 sin pistas, practica en [LeetCode](https://leetcode.com/) o [NeetCode 150](https://neetcode.io/practice), filtrando por los mismos patrones.
