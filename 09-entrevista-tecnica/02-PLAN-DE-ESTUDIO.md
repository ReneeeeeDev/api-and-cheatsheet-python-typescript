# Plan de estudio para la entrevista técnica

Elige el plan según el tiempo que tengas. Todos usan el material de este repositorio. **Regla:** cada día, al menos la mitad del tiempo es **escribir código tú**, no leer.

---

## Si tienes 3 días

| Día | Mañana (2 h) | Tarde (2 h) | Noche (30 min) |
|---|---|---|---|
| 1 | `01-METODO-LIVE-CODING.md`, secciones 2–6 · problemas 1, 6 y 10 | `03-logica/`: ejercicios 11–20 en tu lenguaje | `07-entrevista/BANCO-PREGUNTAS.md`, secciones 2–5 |
| 2 | Problemas 3, 8, 11, 13 y 19 con cronómetro | `08-guia-desde-cero/`: pasos 4, 6 y 7 escritos por ti | Prepara tus 5 historias STAR (sección 9 del método) |
| 3 | Simulacro: 2 problemas al azar de 30 min, grabándote | `03-DEBUGGING-Y-CODE-REVIEW.md` completo · `04-DISENO…`, sección 2 | Repasa la tabla Big-O y tus historias. **Duerme bien.** |

---

## Si tienes 1 semana

| Día | Tema | Práctica | Lectura de apoyo |
|---|---|---|---|
| 1 | Entorno y método | Configura todo con `00-entorno/`; problemas 1, 2, 6 y 7 | `01-METODO-LIVE-CODING.md` completo |
| 2 | Hash y dos punteros | Problemas 3, 4, 5, 8 y 9 · `03-logica` 26 y 43 | `01-cheatsheets/` de tu lenguaje |
| 3 | Ventana, pila y búsqueda binaria | Problemas 10–16 · `03-logica` 21 y 23 | Sección 5 del método (Big-O) |
| 4 | SQL y proyecto web | `03-logica/sql/` ejercicios 1–25 · `08-guia-desde-cero/` pasos 1–5 | `01-cheatsheets/04-sql.md` |
| 5 | Estructuras (listas, árboles, grafos) | Problemas 17–23 | Sección 6 del método (patrones) |
| 6 | Backtracking, DP y diseño | Problemas 24–30 · `04-DISENO…`, secciones 1 y 2 | `03-DEBUGGING-Y-CODE-REVIEW.md` |
| 7 | **Simulacro completo** | `04-simulacro/enunciado.md` en 3 h, o 2 problemas al azar + 1 diseño | Historias STAR + rúbrica (sección 10) |

---

## Si tienes 2 semanas

**Semana 1, fundamentos.** Sigue el plan de 1 semana, pero resuelve cada problema **en los dos lenguajes** (Python y JS). Al terminar cada día, explica en voz alta un problema como si se lo enseñaras a alguien.

**Semana 2, presión real.**

| Día | Actividad |
|---|---|
| 8 | Repite sin mirar los problemas en los que fallaste (revisa la tabla de seguimiento) |
| 9 | `02-proyectos/` → resuelve 1 reto de un proyecto y compáralo con `06-retos-resueltos/` |
| 10 | Simulacro de prueba práctica: `04-simulacro/` en 3 horas, con commits |
| 11 | Code review: revisa tu propio simulacro con la checklist de `03-DEBUGGING…` |
| 12 | Diseño: los 4 ejercicios de `04-DISENO…`, sección 3, dibujados y explicados en voz alta |
| 13 | Simulacro de entrevista con otra persona o grabándote: 1 problema, 1 diseño y 3 preguntas STAR |
| 14 | Repaso ligero: Big-O, patrones, tus historias y preguntas para el entrevistador. Descanso. |

---

## Rutina diaria (45–60 min)

1. **Calentamiento (5 min):** un ejercicio ⭐ de `03-logica/` sin mirar nada.
2. **Problema principal (30 min):** uno de `algoritmos/PROBLEMAS.md` con el método de 6 pasos, en voz alta.
3. **Revisión (10 min):** compara con la solución de referencia. ¿Hay algo más simple? ¿Acertaste la complejidad?
4. **Registro (5 min):** llena la tabla de abajo. Si fallaste, anota **por qué** (no vi el patrón, error de bordes, sintaxis…).

---

## Seguimiento de los 30 problemas

Copia esta tabla a un archivo tuyo (o a Obsidian) y complétala. Repite cada problema hasta que lo resuelvas **sin pistas y en tiempo**.

| # | Problema | Patrón | Intento 1 | Intento 2 | Sin ayuda | Nota |
|---|---|---|---|---|---|---|
| 1 | Contiene duplicado | Hash | | | | |
| 2 | Elemento mayoritario | Hash | | | | |
| 3 | Secuencia consecutiva | Hash | | | | |
| 4 | Subarreglos suma k | Prefijos | | | | |
| 5 | Producto excepto sí mismo | Prefijos | | | | |
| 6 | Mover ceros | Dos punteros | | | | |
| 7 | Fusionar ordenadas | Dos punteros | | | | |
| 8 | Tres suma | Dos punteros | | | | |
| 9 | Contenedor con más agua | Dos punteros | | | | |
| 10 | Máx. suma ventana | Ventana | | | | |
| 11 | Subcadena sin repetir | Ventana | | | | |
| 12 | Evaluar RPN | Pila | | | | |
| 13 | Temperaturas diarias | Pila monótona | | | | |
| 14 | Pila mínima | Diseño + pila | | | | |
| 15 | Raíz entera | Búsqueda binaria | | | | |
| 16 | Buscar en rotado | Búsqueda binaria | | | | |
| 17 | Invertir lista | Lista enlazada | | | | |
| 18 | Detectar ciclo | Lista enlazada | | | | |
| 19 | Altura de árbol | DFS | | | | |
| 20 | Recorrido por niveles | BFS | | | | |
| 21 | ¿Es BST? | DFS + rangos | | | | |
| 22 | Contar islas | BFS/DFS en cuadrícula | | | | |
| 23 | Orden de materias | Orden topológico | | | | |
| 24 | Subconjuntos | Backtracking | | | | |
| 25 | Permutaciones | Backtracking | | | | |
| 26 | Subir escalera | DP | | | | |
| 27 | Subarreglo máximo | DP (Kadane) | | | | |
| 28 | Subsecuencia común | DP 2D | | | | |
| 29 | Merge sort | Divide y vencerás | | | | |
| 30 | Caché LRU | Diseño + hash | | | | |

---

## El día de la entrevista

- [ ] Probé cámara, micrófono, internet y el editor (o la plataforma que usarán: CoderPad, HackerRank, LeetCode).
- [ ] Tengo agua, papel y lápiz para dibujar.
- [ ] Repasé mis 5 historias STAR y 3 preguntas para el entrevistador.
- [ ] Llego (o me conecto) 10 minutos antes.
- [ ] Durante el problema: entender → ejemplos → fuerza bruta → optimizar → programar → probar.
- [ ] Si me bloqueo: lo digo en voz alta y vuelvo al ejemplo.
- [ ] Al final: agradezco y pregunto por los siguientes pasos.
