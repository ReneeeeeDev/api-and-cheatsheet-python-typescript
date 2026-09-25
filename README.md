# Kit de preparación v2 — Técnico en Desarrollo de Software (ISTE)

**Prueba:** viernes 25/09/2026 · 16h00 · 3 horas · 2.º piso, Laboratorio 002 · llegar 15h45 con cédula.

> **Forma más cómoda de leer:** abre `LEEME-PRIMERO.html` en el navegador. Tiene un índice con enlaces a todas las guías en HTML (con botón "Copiar" en cada bloque de código). Los archivos `.md` tienen el mismo contenido para abrirlos en VS Code con `Ctrl + Shift + V`.

## Contenido

| Carpeta | Qué hay | Empieza por |
|---|---|---|
| `00-entorno/` | **Cómo instalar, configurar y ejecutar TODO**: terminal, venv, npm, Java, XAMPP, VS Code, probar APIs, depurar, qué hacer si algo falla en el laboratorio | `GUIA-ENTORNO-Y-EJECUCION.md` |
| `01-cheatsheets/` | 12 cheatsheets (~4 300 líneas): Python, JS/Node/Express, React/Next, SQL, Git, HTML/CSS, WordPress/PHP/Java/C# (resumen), **PHP completo, TypeScript, Java ampliado (JDBC, Maven, Spring), C#/.NET, Dart/Flutter + WordPress a fondo + Azure/Vercel + QA** | el de tu lenguaje fuerte + `04-sql.md` |
| `02-proyectos/` | 5 proyectos funcionando: Flask, Express, React, Java consola, **PHP + PDO (nuevo)** | el README de cada uno |
| `03-logica/` | 30 + **20 ejercicios nuevos** (Python y JS con pruebas), SQL: 15 + **25 ejercicios nuevos**, versión MySQL y ejecutor de SQL | `ejercicios.md`, `ejercicios_extra.md`, `sql/README.md` |
| `04-simulacro/` | Enunciado de prueba de 3 h, plantillas de un archivo, solución Flask | `enunciado.md` |
| `05-ejemplos/` | **24 programas ejecutables** que demuestran cada tema de los cheatsheets (Python, JS, Java, PHP, TS, DOM) | `README.md` |
| `06-retos-resueltos/` | **Soluciones de los retos** de los 4 proyectos, cada una con RETOS.md explicativo | `README.md` |
| `07-entrevista/` | **Banco de ~100 preguntas** con respuestas cortas (técnicas, situacionales, sobre ti) | `BANCO-PREGUNTAS.md` |
| `08-guia-desde-cero/` | Guías paso a paso para construir el simulacro desde cero (Flask y Express) con solucionario | `GUIA-1-FLASK.md` o `GUIA-2-EXPRESS.md` |

## Todo verificado
- Proyectos: Flask (9 pruebas), Express (8), React (build), Java (9), PHP (probado con `php -S`).
- Retos resueltos: Flask (12 pruebas), Express (12), React (build + navegador), Java (19).
- Guías desde cero: Flask (14), Express (14), seguidas paso a paso.
- Lógica: 30/30 y 21/21 casos en Python y JS. SQL: los 40 ejercicios corren sin errores en SQLite.
- Los 24 ejemplos se ejecutaron sin errores.

## Plan para las horas que quedan (ajústalo a tu hora actual)

| Tiempo | Actividad |
|---|---|
| 20 min | `00-entorno`: partes 2, 4 (venv) y 10 (checklist del laboratorio). Así evitas perder tiempo configurando. |
| 45 min | En `08-guia-desde-cero`, en tu lenguaje, **escribe tú** los pasos 4, 6 y 7 (validaciones, CRUD, reservas). |
| 20 min | SQL: ejercicios 16–25 de `ejercicios_extra.sql` (JOIN, GROUP BY, LEFT JOIN, HAVING). |
| 20 min | Lógica: ejercicios 32, 35, 36 y 39 (factura, conflictos, intervalos, password). |
| 15 min | `07-entrevista`: secciones 1, 4 y 5. |
| **Descanso** | Come, hidrátate, sal con tiempo. No estudies en el bus: repasa solo la checklist. |

## Checklist en la prueba
1. Leer todo el enunciado. Subrayar lo obligatorio.
2. Verificar herramientas (`python --version`, `node -v`, XAMPP, internet).
3. Diseñar tablas y rutas en papel (5 min).
4. `git init` y el primer commit en los primeros 10 minutos.
5. Hacer funcionar **listar y crear** primero; luego editar/eliminar; después las reglas de negocio; al final lo extra.
6. Validar en el servidor. Consultas parametrizadas. Commit cada vez que algo funcione.
7. README con cómo ejecutarlo.
8. Últimos 20 minutos: probar todo como usuario, sin agregar funciones nuevas.

¡Éxitos!
