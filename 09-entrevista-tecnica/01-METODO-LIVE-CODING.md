# Método para la entrevista técnica

Una entrevista técnica no es un examen de memoria: el entrevistador quiere ver **cómo piensas, cómo te comunicas y si tu código funciona**. Una solución "regular" bien explicada y probada suele puntuar mejor que una óptima escrita en silencio.

---

## 1. Tipos de entrevista y cómo prepararte

| Etapa | Qué evalúan | Dura | Practica con |
|---|---|---|---|
| Filtro con RR. HH. | Comunicación, interés, expectativas | 15–30 min | `07-entrevista/BANCO-PREGUNTAS.md`, sección 1 |
| Preguntas técnicas (conceptos) | Fundamentos: POO, SQL, HTTP, Git, tu stack | 30–45 min | `07-entrevista/BANCO-PREGUNTAS.md` + `01-cheatsheets/` |
| **Live coding** (pantalla compartida o pizarra) | Resolver un problema pensando en voz alta | 45–60 min | `algoritmos/` + `03-logica/` + este método |
| Prueba práctica (laboratorio o para casa) | Construir un CRUD o API completa con reglas de negocio | 2–4 h o 2–7 días | `04-simulacro/`, `08-guia-desde-cero/`, `02-proyectos/` |
| Code review / debugging | Encontrar errores y mejorar código ajeno | 30–45 min | [03-DEBUGGING-Y-CODE-REVIEW.md](03-DEBUGGING-Y-CODE-REVIEW.md) |
| Diseño de sistemas (junior) | Modelar datos, diseñar una API y pensar en escala | 30–45 min | [04-DISENO-DE-SISTEMAS-JUNIOR.md](04-DISENO-DE-SISTEMAS-JUNIOR.md) |
| Conductual / cultura | Trabajo en equipo, manejo de errores, aprendizaje | 30 min | Sección 9 de este documento |

---

## 2. Los 6 pasos para resolver un problema en vivo

Para un problema de 45 minutos, los tiempos aproximados son:

| Paso | Tiempo | Qué haces | Qué dices |
|---|---|---|---|
| **1. Entender** | 3–5 min | Repetir el problema con tus palabras y preguntar las restricciones | "Para confirmar: recibo… y devuelvo…. ¿Puede venir vacío? ¿Hay negativos?" |
| **2. Ejemplos** | 2–3 min | Un ejemplo normal y uno de borde, resueltos a mano | "Con [2, 7, 11] y 9 debería devolver [0, 1]. ¿Y si no hay solución?" |
| **3. Fuerza bruta** | 2 min | Decir la solución obvia y su complejidad, **sin programarla** | "Lo directo son dos bucles, O(n²). Funciona, pero creo que se puede mejorar." |
| **4. Optimizar** | 5–10 min | Encontrar el trabajo repetido y elegir el patrón (sección 6) | "Estoy buscando el complemento una y otra vez; con un diccionario cada búsqueda es O(1)." |
| **5. Programar** | 15–20 min | Código limpio, narrando lo que haces | "Ahora recorro la lista; para cada número calculo el complemento…" |
| **6. Probar** | 5 min | Recorrer el código a mano con el ejemplo, casos de borde y complejidad final | "Con [2, 7]: i=0 guarda 2→0; i=1 busca 2, existe → [0, 1]. Queda O(n) en tiempo y en memoria." |

> **Regla de oro:** no empieces a programar hasta que el entrevistador esté de acuerdo con tu enfoque. "¿Te parece bien si lo implemento así?"

---

## 3. Preguntas para aclarar el enunciado

Antes de programar, revisa con el entrevistador:

- **Entrada:** ¿tipo? ¿Puede estar vacía o ser `None` / `null`? ¿Tamaño máximo (100 o 10 millones)?
- **Valores:** ¿negativos, ceros o repetidos? ¿Letras con tildes, mayúsculas o espacios?
- **¿Viene ordenada?** Si sí, piensa en búsqueda binaria o dos punteros.
- **Salida:** ¿qué devuelvo si no hay respuesta (−1, `None`, `[]` o una excepción)? Si hay varias respuestas, ¿importa el orden?
- **Restricciones:** ¿puedo modificar la entrada? ¿Puedo usar librerías (`sort`, `Counter`)? ¿Hay un límite de memoria?

---

## 4. Frases para pensar en voz alta

| Situación | Frase |
|---|---|
| Empiezas | "Déjame asegurarme de entender bien el problema…" |
| Propones algo | "Una primera idea es…, que sería O(…). ¿Quieres que la implemente o busco algo mejor?" |
| Te bloqueas | "Estoy entre dos opciones: A, que…, y B, que…. Me inclino por A porque…" |
| Te equivocas | "Aquí veo un error: con un arreglo vacío esto falla. Lo corrijo así…" |
| No sabes algo | "No recuerdo la sintaxis exacta de…; en pseudocódigo sería así. ¿Puedo asumirla?" |
| Recibes una pista | "Buena observación; entonces, si uso…, puedo evitar…" |
| Terminas | "Lo pruebo con el ejemplo y con los casos de borde. La complejidad final es…" |
| Sobra tiempo | "Si esto fuera a producción, agregaría validación de la entrada y pruebas para…" |

---

## 5. Big-O de bolsillo

| Complejidad | Nombre | Ejemplo | n = 1 000 000 |
|---|---|---|---|
| O(1) | Constante | Acceso por índice, buscar en dict/set | instantáneo |
| O(log n) | Logarítmica | Búsqueda binaria | ~20 pasos |
| O(n) | Lineal | Recorrer una vez | 1 millón |
| O(n log n) | Linealítmica | `sort()`, merge sort | ~20 millones |
| O(n²) | Cuadrática | Dos bucles anidados | 10¹² → **demasiado lento** |
| O(2ⁿ) | Exponencial | Subconjuntos, Fibonacci recursivo sin memoria | imposible si n > ~30 |

**Regla práctica:** cerca de 10⁸ operaciones simples por segundo (Python es unas 10–50 veces más lento). Si n ≤ 10⁵, necesitas O(n log n) o menos.

### Costo de las operaciones en Python y JavaScript

| Operación | Python | JavaScript | Costo |
|---|---|---|---|
| Acceso por índice | `lista[i]` | `arr[i]` | O(1) |
| Agregar / quitar al final | `append` / `pop()` | `push` / `pop` | O(1) |
| Agregar / quitar al inicio | `insert(0, x)` / `pop(0)` | `unshift` / `shift` | **O(n)**: usa `deque` |
| Buscar un valor en una lista | `x in lista` | `arr.includes(x)` | **O(n)** |
| Buscar en un diccionario o set | `x in d` / `x in s` | `map.has(x)` / `set.has(x)` | O(1) promedio |
| Ordenar | `sorted(l)` / `l.sort()` | `arr.sort((a, b) => a - b)` | O(n log n) |
| Copiar o cortar | `lista[a:b]`, `lista.copy()` | `slice`, `[...arr]` | O(k) |
| Concatenar texto en un bucle | `s += c` | `s += c` | puede ser O(n²): usa `"".join(partes)` / `partes.join("")` |
| Cola eficiente | `collections.deque` (`popleft`) | arreglo + índice de lectura | O(1) |
| Mínimo o máximo dinámico | `heapq` | (sin heap nativo) | O(log n) |

> **Cuidado en JS:** `[10, 9, 1].sort()` devuelve `[1, 10, 9]` porque ordena como texto. Siempre usa `sort((a, b) => a - b)`.

---

## 6. Reconocer el patrón

| Si el enunciado dice… | Piensa en… | Problemas |
|---|---|---|
| "¿Existe…?", "contar", "pares que suman X" | **Diccionario / set** | 1–5, 03-logica #26 |
| Arreglo **ordenado**, "pares", "en el mismo arreglo" | **Dos punteros** | 6–9 |
| "Subarreglo/subcadena **contigua** más larga/corta con…" | **Ventana deslizante** | 10–11 |
| "Suma de un tramo", "subarreglos que suman k" | **Sumas prefijas** | 4 |
| Paréntesis, expresiones, "el siguiente mayor", deshacer | **Pila** | 12–14, 03-logica #23 |
| Ordenado + "O(log n)", "el menor valor que cumple…" | **Búsqueda binaria** | 15–16, 03-logica #21 |
| Árbol, "profundidad", "camino" | **DFS recursivo** | 19, 21 |
| "Por niveles", "camino más corto sin pesos" | **BFS con cola** | 20, 22 |
| Dependencias, "orden válido", requisitos | **Orden topológico** | 23 |
| "**Todas** las combinaciones/permutaciones" | **Backtracking** | 24–25 |
| "¿De cuántas formas…?", "máximo/mínimo" con subproblemas repetidos | **Programación dinámica** | 26–28, 03-logica #44 |
| "Intervalos", "reuniones", "reservas que chocan" | **Ordenar por inicio** | 03-logica #35 y #36 |
| "Los k más frecuentes / más grandes" | **Heap** o `Counter.most_common` | 03-logica #37 |

### Plantillas que conviene escribir de memoria

```python
# Dos punteros sobre un arreglo ordenado
izq, der = 0, len(a) - 1
while izq < der:
    if condicion(a[izq], a[der]): ...; izq += 1
    else: der -= 1

# Ventana deslizante de tamaño variable
inicio = 0
for fin, x in enumerate(a):
    agregar(x)
    while ventana_invalida():
        quitar(a[inicio]); inicio += 1
    mejor = max(mejor, fin - inicio + 1)

# Búsqueda binaria "el mayor valor que cumple"
izq, der = minimo, maximo
while izq <= der:
    medio = (izq + der) // 2
    if cumple(medio): izq = medio + 1
    else: der = medio - 1
return der

# BFS (en grafos o cuadrículas)
from collections import deque
cola, visitados = deque([inicio]), {inicio}
while cola:
    actual = cola.popleft()
    for vecino in vecinos(actual):
        if vecino not in visitados:
            visitados.add(vecino); cola.append(vecino)

# Backtracking
def explorar(estado):
    if es_solucion(estado): resultado.append(estado.copy()); return
    for opcion in opciones(estado):
        elegir(opcion); explorar(estado); deshacer(opcion)
```

---

## 7. Casos de borde que siempre debes probar

- Vacío: `[]`, `""`, `None`, árbol o lista enlazada nula.
- Un solo elemento, o dos elementos.
- Todos iguales; todos distintos.
- Negativos, cero, números muy grandes.
- Ya ordenado y ordenado al revés.
- Sin solución; varias soluciones.
- Texto con mayúsculas, tildes o espacios al inicio y al final.

---

## 8. Errores que más restan puntos

1. Programar en silencio durante 10 minutos.
2. Empezar a programar sin ejemplos ni preguntas: terminas resolviendo otro problema.
3. Defender una idea equivocada en lugar de aceptar la pista.
4. Nombres como `a`, `x2` o `temp` en todo el código. Usa `izq`, `der`, `vistos`, `conteo`.
5. No probar: decir "creo que funciona" sin recorrer un ejemplo.
6. No dar la complejidad, o darla mal (un `in` sobre una lista dentro de un bucle ya es O(n²)).
7. Quedarte callado al bloquearte. Di qué estás pensando: el entrevistador puede ayudarte.

**Si te bloqueas:** vuelve al ejemplo y resuélvelo a mano, despacio. ¿Qué hiciste en tu cabeza? Eso es el algoritmo. Si aun así no sale, implementa la fuerza bruta: código funcionando vale más que una idea óptima a medias.

---

## 9. Parte conductual: el método STAR

Responde en 1–2 minutos con esta estructura:

| Letra | Qué cuentas | Peso |
|---|---|---|
| **S**ituación | Contexto breve: proyecto, equipo, problema | 15 % |
| **T**area | Cuál era **tu** responsabilidad | 10 % |
| **A**cción | Qué hiciste **tú** (en primera persona), con detalles técnicos | 60 % |
| **R**esultado | Qué pasó, con números si puedes, y qué aprendiste | 15 % |

### Prepara 5 historias que cubran casi todo

| # | Tema de la historia | Responde a preguntas como… |
|---|---|---|
| 1 | Un proyecto del que estés orgulloso | "Háblame de tu mejor proyecto", "¿Qué logro destacas?" |
| 2 | Un bug o problema difícil que resolviste | "¿Cuál fue tu mayor reto técnico?", "¿Cómo depuras?" |
| 3 | Un error tuyo y cómo lo corregiste | "Cuéntame de un fracaso", "¿Cuál es tu debilidad?" |
| 4 | Un desacuerdo o conflicto en un equipo | "¿Cómo manejas los conflictos?", "Trabajo en equipo" |
| 5 | Algo que aprendiste rápido por necesidad | "¿Cómo aprendes?", "Plazo ajustado", "Tecnología nueva" |

Plantilla para escribir cada historia (llénala en un documento aparte):

```text
Historia: ______________________
S: ______________________________________________
T: ______________________________________________
A: (3 acciones concretas, en primera persona)
   1. ____________________________________________
   2. ____________________________________________
   3. ____________________________________________
R: (número o resultado visible + lo que aprendí) ___
```

### Preguntas para hacerle al entrevistador (elige 2 o 3)

- ¿Cómo es un día normal de alguien en este puesto?
- ¿Cómo trabajan el control de versiones, las revisiones de código y los despliegues?
- ¿Qué tendría que lograr en mis primeros 3 meses para que consideren que me fue bien?
- ¿Cuál es el mayor reto técnico del equipo ahora mismo?
- ¿Cómo apoyan el aprendizaje (mentorías, cursos, tiempo para formación)?

---

## 10. Rúbrica para autoevaluarte después de cada simulacro

Califícate de 1 a 4 en cada fila; tu objetivo es tener 3 o más en todas.

| Criterio | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **Comprensión** | Empecé sin preguntar | Pregunté algo | Aclaré la entrada, la salida y los bordes | Además propuse ejemplos propios |
| **Comunicación** | Estuve callado | Expliqué a ratos | Narré todo el proceso | Fue claro y conversado, y acepté pistas |
| **Solución** | No llegué a nada | Solo la fuerza bruta | Llegué a la óptima con ayuda | Llegué a la óptima solo y justifiqué el patrón |
| **Código** | No funciona | Funciona, pero es confuso | Limpio y con buenos nombres | Limpio, modular y maneja los bordes |
| **Pruebas** | No probé | Probé un caso | Recorrí un ejemplo y los bordes | Encontré y corregí mis propios errores |
| **Complejidad** | No la mencioné | La dije mal | Correcta en tiempo | Correcta en tiempo y memoria, con alternativas |

### Cómo hacer un simulacro

- **Solo:** elige un problema al azar de `algoritmos/PROBLEMAS.md`, pon 30 minutos y **grábate** (audio o pantalla con OBS). Al escucharte notarás silencios y muletillas.
- **Con alguien:** que esa persona lea el enunciado en voz alta, no te muestre la solución y te dé solo una pista si llevas 5 minutos sin avanzar. Después, que llene la rúbrica.
- **Con IA:** pídele que actúe como entrevistador, que te dé un problema sin la solución y que evalúe tu explicación con esta rúbrica.
