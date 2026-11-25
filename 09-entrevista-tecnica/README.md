# 09 · Entrevista técnica: método, algoritmos, debugging y diseño

Esta sección te prepara para la parte **en vivo** de la entrevista: resolver problemas pensando en voz alta, revisar código ajeno y diseñar un sistema pequeño. Complementa la prueba práctica (`04-simulacro/`, `08-guia-desde-cero/`) y las preguntas conceptuales (`07-entrevista/`).

| Archivo | Qué contiene | Cuándo usarlo |
|---|---|---|
| [01-METODO-LIVE-CODING.md](01-METODO-LIVE-CODING.md) | Los 6 pasos para resolver en vivo, frases para pensar en voz alta, Big-O, cómo reconocer el patrón, plantillas de código, método STAR y rúbrica de autoevaluación | **Primero.** Léelo completo una vez y vuelve a las tablas antes de cada práctica |
| [02-PLAN-DE-ESTUDIO.md](02-PLAN-DE-ESTUDIO.md) | Planes de 3 días, 1 semana y 2 semanas, rutina diaria, tabla de seguimiento y checklist del día de la entrevista | Para organizarte |
| [algoritmos/PROBLEMAS.md](algoritmos/PROBLEMAS.md) | **30 problemas clásicos por patrón** con pistas, plantillas para practicar, pruebas automáticas y soluciones en Python y JavaScript | Todos los días |
| [03-DEBUGGING-Y-CODE-REVIEW.md](03-DEBUGGING-Y-CODE-REVIEW.md) | 15 errores clásicos de Python y JS, un ejercicio de code review con 12 problemas y una checklist de revisión | Antes de entrevistas con revisión de código |
| [04-DISENO-DE-SISTEMAS-JUNIOR.md](04-DISENO-DE-SISTEMAS-JUNIOR.md) | Método en 5 pasos, sistema de reservas resuelto, 4 ejercicios más, conceptos clave y OWASP Top 10 | Cuando te pregunten "¿cómo diseñarías…?" |

## Empezar en 2 minutos

```bash
cd 09-entrevista-tecnica/algoritmos
python pruebas.py                         # las soluciones de referencia: 30/30
copy plantilla.py mis_soluciones.py       # tu archivo de práctica (Linux/Mac: cp)
python pruebas.py mis_soluciones 1        # resuelve el 1 y pruébalo
```

En JavaScript: `node pruebas.js` y `node pruebas.js mis_soluciones.js 1` (solo necesitas Node 18 o superior, sin `npm install`).

## Qué hay en las pruebas

- Cada problema tiene entre 2 y 6 casos, incluidos los de borde (vacíos, negativos, un elemento, sin solución).
- El resultado muestra `OK`, `FALLO` (con lo esperado y lo obtenido) o `PENDIENTE` (todavía no lo resuelves).
- Las soluciones de referencia se verifican automáticamente en GitHub Actions en cada push (ver `.github/workflows/`).
