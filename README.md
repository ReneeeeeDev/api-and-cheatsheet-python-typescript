# Kit de preparación — Entrevista técnica de desarrollo de software

[![Pruebas](https://github.com/ReneeeeeDev/api-and-cheatsheet-python-typescript/actions/workflows/pruebas.yml/badge.svg)](https://github.com/ReneeeeeDev/api-and-cheatsheet-python-typescript/actions/workflows/pruebas.yml)

Material para prepararse **de principio a fin** para una entrevista técnica de desarrollador junior o semi-senior: fundamentos por tecnología, lógica y SQL, proyectos CRUD completos, una prueba práctica cronometrada, algoritmos para *live coding*, debugging, diseño de sistemas y preguntas de entrevista. Todo en español y con código que se ejecuta y se prueba.

> **Forma más cómoda de leer:** abre `LEEME-PRIMERO.html` en el navegador. Tiene un índice con enlaces a todas las guías en HTML, con botón "Copiar" en cada bloque de código. Los archivos `.md` tienen el mismo contenido; en VS Code se ven con `Ctrl + Shift + V`.

## ¿Por dónde empiezo?

| Tu situación | Empieza por |
|---|---|
| Tengo una entrevista pronto y no sé cómo organizarme | [`09-entrevista-tecnica/02-PLAN-DE-ESTUDIO.md`](09-entrevista-tecnica/02-PLAN-DE-ESTUDIO.md) (planes de 3 días, 1 semana y 2 semanas) |
| Me van a poner a programar en vivo | [`09-entrevista-tecnica/01-METODO-LIVE-CODING.md`](09-entrevista-tecnica/01-METODO-LIVE-CODING.md) → [`algoritmos/PROBLEMAS.md`](09-entrevista-tecnica/algoritmos/PROBLEMAS.md) |
| Me van a dar una prueba práctica (construir una app en 2–4 h) | [`08-guia-desde-cero/`](08-guia-desde-cero/LEEME.md) → [`04-simulacro/`](04-simulacro/enunciado.md) |
| Quiero repasar la teoría para las preguntas | [`07-entrevista/BANCO-PREGUNTAS.md`](07-entrevista/BANCO-PREGUNTAS.md) + el cheatsheet de tu lenguaje |
| Primero necesito instalar y configurar todo | [`00-entorno/GUIA-ENTORNO-Y-EJECUCION.md`](00-entorno/GUIA-ENTORNO-Y-EJECUCION.md) |

## Contenido

| Carpeta | Qué hay | Empieza por |
|---|---|---|
| `00-entorno/` | **Cómo instalar, configurar y ejecutar TODO**: terminal, venv, npm, Java, XAMPP, VS Code, probar APIs, depurar y qué hacer si algo falla en el laboratorio | `GUIA-ENTORNO-Y-EJECUCION.md` |
| `01-cheatsheets/` | 12 cheatsheets (~4 300 líneas): Python, JS/Node/Express, React/Next, SQL, Git, HTML/CSS, PHP, TypeScript, Java (JDBC, Maven, Spring), C#/.NET, Dart/Flutter, WordPress, Azure/Vercel y QA | el de tu lenguaje fuerte + `04-sql.md` |
| `02-proyectos/` | 5 proyectos funcionando: Flask, Express, React, Java consola y PHP + PDO | el README de cada uno |
| `03-logica/` | 50 ejercicios de lógica (Python y JS, con pruebas) y 40 de SQL, con versión MySQL y un ejecutor de SQL | `ejercicios.md`, `ejercicios_extra.md`, `sql/README.md` |
| `04-simulacro/` | Enunciado de una prueba práctica de 3 h, plantillas de un archivo y solución en Flask | `enunciado.md` |
| `05-ejemplos/` | **24 programas ejecutables** que demuestran cada tema de los cheatsheets (Python, JS, Java, PHP, TS, DOM) | `README.md` |
| `06-retos-resueltos/` | **Soluciones de los retos** de los 4 proyectos, cada una con un RETOS.md que explica los cambios | `README.md` |
| `07-entrevista/` | **Banco de ~120 preguntas** con respuestas cortas: sobre ti, programación, POO, bases de datos, web, JS, Python/PHP, Git, pruebas, algoritmos y situaciones | `BANCO-PREGUNTAS.md` |
| `08-guia-desde-cero/` | Guías paso a paso para construir una app de reservas desde cero (Flask y Express), con solucionario y 14 pruebas cada una | `GUIA-1-FLASK.md` o `GUIA-2-EXPRESS.md` |
| `09-entrevista-tecnica/` | **Nuevo.** Método para *live coding*, **30 problemas clásicos por patrón** con plantillas, pruebas automáticas y soluciones en Python y JS, 15 errores para depurar, un ejercicio de code review, diseño de sistemas junior, OWASP Top 10, STAR y rúbrica | `README.md` |
| `mi-practica/` | Mis intentos (separados de las soluciones) y su avance | `README.md` |
| `_herramientas/` | `generar_html.py`: regenera los `.html` y el índice a partir de los `.md` | — |

## Probar que todo funciona

```bash
# Algoritmos de entrevista (sin instalar nada)
cd 09-entrevista-tecnica/algoritmos
python pruebas.py            # 30/30
node pruebas.js              # 30/30

# Lógica
cd ../../03-logica
python soluciones.py && python soluciones_extra.py
node soluciones.js && node soluciones_extra.js

# App Flask del solucionario
cd ../08-guia-desde-cero/solucionario/reservas-flask
python -m venv venv && venv\Scripts\activate      # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt && pytest -q
```

GitHub Actions ejecuta estas pruebas en cada push (insignia "Pruebas" de arriba).

## Regenerar los HTML

Si editas un `.md`, regenera su `.html` y el índice:

```bash
pip install markdown pygments
python _herramientas/generar_html.py
```

## Cómo usar este kit sin engañarte

1. **Escribe el código tú.** Leer una solución da la falsa sensación de que "ya lo sabes". Usa `plantilla.py`/`plantilla.js` y la carpeta `mi-practica/`.
2. **Cronométrate y habla en voz alta**, como en la entrevista real.
3. **Registra tus fallos** (tabla del plan de estudio) y repite esos problemas días después.
4. Haz al menos **un simulacro completo** (`04-simulacro/`) antes de una prueba práctica.
