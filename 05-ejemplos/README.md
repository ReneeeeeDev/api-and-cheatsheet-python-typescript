# Ejemplos ejecutables de los cheatsheets

Cada archivo es un programa completo que **imprime** el resultado de cada concepto, con comentarios que indican lo que debería salir. Léelo, ejecútalo y luego modifícalo para ver qué cambia.

| Archivo | Tema | Comando | Requisito |
|---|---|---|---|
| `python/01_basicos.py` | Tipos, operadores, formato, if/match, bucles | `python 01_basicos.py` | Python 3.10+ |
| `python/02_colecciones.py` | Listas, dict, set, tuplas, comprehensions, CRUD en memoria | `python 02_colecciones.py` | |
| `python/03_strings.py` | Métodos de texto, tildes, ejercicios típicos | `python 03_strings.py` | |
| `python/04_funciones_errores.py` | *args, **kwargs, closures, recursión, decoradores, excepciones | `python 04_funciones_errores.py` | |
| `python/05_poo.py` | Encapsulamiento, herencia, abstracción, polimorfismo, dataclass | `python 05_poo.py` | |
| `python/06_archivos_json_csv.py` | Texto, JSON, CSV (crea `salida_06/`) | `python 06_archivos_json_csv.py` | |
| `python/07_sqlite_crud.py` | CRUD SQLite, JOIN, transacciones, SQL Injection | `python 07_sqlite_crud.py` o `python 07_sqlite_crud.py menu` | |
| `python/08_fechas_regex_modulos.py` | datetime, regex, random, Decimal | `python 08_fechas_regex_modulos.py` | |
| `python/09_estructuras_datos.py` | Pila, cola, lista enlazada, búsquedas, 5 ordenamientos | `python 09_estructuras_datos.py` | |
| `python/10_servidor_sin_flask.py` | Servidor web + API sin instalar nada | `python 10_servidor_sin_flask.py` → http://localhost:8000 | |
| `javascript/01_basicos.js` | Tipos, ===, truthy, ??, ?., bucles, switch | `node 01_basicos.js` | Node 18+ |
| `javascript/02_arrays.js` | map/filter/reduce, sort, agrupar, CRUD inmutable | `node 02_arrays.js` | |
| `javascript/03_objetos_strings.js` | Objetos, spread, JSON, Map/Set, strings | `node 03_objetos_strings.js` | |
| `javascript/04_funciones_closures.js` | Arrow, closures, debounce, this, recursión, errores | `node 04_funciones_closures.js` | |
| `javascript/05_clases.js` | Clases, #privados, getters, herencia, repositorio | `node 05_clases.js` | |
| `javascript/06_async.js` | Event loop, promesas, async/await, Promise.all, fetch | `node 06_async.js` | internet para fetch |
| `javascript/07_archivos_modulos.mjs` | fs, path, JSON como BD, import/export, env | `node 07_archivos_modulos.mjs` | |
| `javascript/08_fechas_regex.js` | Date, Intl, regex | `node 08_fechas_regex.js` | |
| `javascript/09_node_sqlite.mjs` | SQLite sin npm (node:sqlite) | `node 09_node_sqlite.mjs` | **Node 22.5+** |
| `javascript/10_servidor_sin_express.js` | Servidor + API REST con `http` puro | `node 10_servidor_sin_express.js` → http://localhost:8001 | |
| `java/Basicos.java` | Todo Java: strings, colecciones, streams, POO, records, fechas | `java Basicos.java` | JDK 17+ |
| `php/basicos.php` | Todo PHP: arrays, POO, excepciones, JSON, PDO | `php basicos.php` | PHP 8.1+ |
| `typescript/basicos.ts` | Tipos, interfaces, genéricos, utilidades | `npx tsx basicos.ts` | Node + internet |
| `web-dom/index.html` | DOM, eventos, validación, localStorage, CSV, fetch | Doble clic (se abre en el navegador) | Navegador |

## Cómo sacarles provecho
1. Ejecuta el archivo y compara la salida con los comentarios `# ...` / `// ...`.
2. Cambia valores y vuelve a ejecutar.
3. Rehaz las funciones de los "ejercicios típicos" sin mirar.
4. Para ejecutar solo un fragmento: copia las líneas en la consola interactiva (`python` o `node`).
