# Guía de entorno y ejecución: cómo instalar, configurar y correr TODO el kit

Esta guía asume **Windows 10/11**, que es lo más probable en el laboratorio. Para cada comando también está la versión de Linux/Mac cuando es distinta.

---

## Parte 1. Conceptos que debes tener claros

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Terminal / consola** | Programa donde escribes comandos | PowerShell, CMD, Git Bash, terminal de VS Code |
| **Intérprete** | Programa que ejecuta tu código línea por línea | `python`, `node`, `php` |
| **Compilador** | Traduce el código antes de ejecutarlo | `javac` (Java), `tsc` (TypeScript), `dotnet build` (C#) |
| **Gestor de paquetes** | Instala librerías de terceros | `pip` (Python), `npm` (Node), `composer` (PHP), `maven` (Java) |
| **Entorno virtual** | Carpeta aislada con las librerías de UN proyecto | `venv` en Python; en Node la carpeta `node_modules` cumple ese papel |
| **Servidor web local** | Programa que atiende peticiones HTTP en tu PC | Flask en `:5000`, Express en `:3000`, Apache/XAMPP en `:80`, Vite en `:5173` |
| **localhost / 127.0.0.1** | "Esta misma computadora" | `http://localhost:3000` |
| **Puerto** | Número que identifica qué programa atiende | 3000, 5000, 5173, 80, 3306 (MySQL) |
| **PATH** | Lista de carpetas donde Windows busca los comandos | Si `python` "no se reconoce", no está en el PATH |
| **Directorio actual** | Carpeta en la que "estás" en la terminal | Se ve en el prompt: `PS C:\Users\Ana\Desktop>` |

**Regla de oro:** casi todos los errores al ejecutar son por (1) estar en la carpeta equivocada, (2) no haber instalado las dependencias o (3) no haber activado el entorno virtual.

---

## Parte 2. La terminal en 5 minutos

### Abrir una terminal
- **Dentro de VS Code** (recomendado): menú *Terminal → New Terminal*, o `Ctrl + ñ` (teclado en español) / `` Ctrl + ` ``.
- **En una carpeta**: abre la carpeta en el Explorador de Windows, escribe `cmd` o `powershell` en la barra de dirección y presiona Enter. La terminal se abre ya en esa carpeta.
- **Shift + clic derecho** dentro de una carpeta → "Abrir en Terminal".

### Comandos básicos

| Acción | PowerShell / CMD | Linux / Mac / Git Bash |
|---|---|---|
| Ver dónde estoy | `pwd` (PS) / `cd` (CMD) | `pwd` |
| Listar archivos | `dir` o `ls` (PS) | `ls -la` |
| Entrar a una carpeta | `cd nombre` | `cd nombre` |
| Subir un nivel | `cd ..` | `cd ..` |
| Ir al escritorio | `cd $HOME\Desktop` (PS) | `cd ~/Desktop` |
| Crear carpeta | `mkdir nombre` | `mkdir -p a/b/c` |
| Crear archivo vacío | `ni archivo.txt` (PS) / `type nul > archivo.txt` (CMD) | `touch archivo.txt` |
| Ver contenido | `type archivo.txt` / `cat` (PS) | `cat archivo.txt` |
| Borrar archivo | `del archivo.txt` | `rm archivo.txt` |
| Borrar carpeta | `rmdir /s carpeta` (CMD) / `rm -r carpeta` (PS) | `rm -rf carpeta` |
| Limpiar pantalla | `cls` | `clear` |
| Abrir carpeta en VS Code | `code .` | `code .` |
| Detener un programa | `Ctrl + C` | `Ctrl + C` |
| Repetir comando anterior | flecha ↑ | flecha ↑ |
| Autocompletar nombre | `Tab` | `Tab` |

**Rutas con espacios** van entre comillas: `cd "C:\Users\Ana\Mis Proyectos"`.

---

## Parte 3. Instalar las herramientas (si la PC no las tiene)

En el laboratorio seguramente ya estarán instaladas. Lo primero es **verificar**:

```bash
python --version      # o: py --version
pip --version         # o: python -m pip --version
node -v
npm -v
java -version
javac -version
git --version
php -v                # si hay XAMPP: C:\xampp\php\php.exe -v
code --version
```

### Python
1. https://www.python.org/downloads/ → descargar Python 3.12 o 3.13.
2. **MUY IMPORTANTE:** en la primera pantalla del instalador marca **"Add python.exe to PATH"**.
3. Cierra y vuelve a abrir la terminal → `python --version`.

Si `python` abre la Microsoft Store o "no se reconoce":
- Prueba `py --version` (el lanzador de Windows). Si funciona, usa `py` en lugar de `python` en todo el kit.
- O desactívalo en *Configuración → Aplicaciones → Alias de ejecución de aplicaciones →* apagar "python.exe" y "python3.exe".

### Node.js
1. https://nodejs.org → descargar la versión **LTS** (22.x).
2. Instalar con las opciones por defecto (incluye `npm`).
3. Nueva terminal → `node -v` y `npm -v`.

Si PowerShell dice *"npm.ps1 no se puede cargar porque la ejecución de scripts está deshabilitada"*:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
O usa **CMD** en lugar de PowerShell.

### Java (JDK)
1. https://adoptium.net → **Temurin JDK 21 (LTS)** → instalador `.msi`.
2. En el instalador, activa **"Set JAVA_HOME"** y **"Add to PATH"**.
3. Nueva terminal → `java -version` y `javac -version`. Necesitas `javac`: si solo tienes `java`, instalaste un JRE y no el JDK.

### Git
1. https://git-scm.com → instalar con opciones por defecto (incluye **Git Bash**).
2. Configura tu identidad (una vez por PC):
   ```bash
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu@correo.com"
   ```

### XAMPP (PHP + MySQL + Apache)
1. https://www.apachefriends.org → instalar en `C:\xampp`.
2. Abrir **XAMPP Control Panel** → **Start** en Apache y MySQL (se ponen en verde).
3. phpMyAdmin: http://localhost/phpmyadmin (usuario `root`, contraseña vacía).
4. Tus archivos PHP van en `C:\xampp\htdocs\mi-proyecto\` → http://localhost/mi-proyecto/

### VS Code + extensiones recomendadas
Instala desde el panel de extensiones (`Ctrl + Shift + X`):
- **Python** (Microsoft): ejecutar y depurar Python.
- **Pylance**: autocompletado de Python.
- **ES7+ React/Redux snippets**: atajos como `rafce`.
- **EJS language support**: colores en archivos `.ejs`.
- **Extension Pack for Java** (Microsoft): ejecutar Java con un botón.
- **SQLite Viewer** (Florian Klampfer): abrir archivos `.db` y ver las tablas.
- **Thunder Client**: probar APIs (como Postman) dentro de VS Code.
- **Live Server**: abrir HTML con recarga automática.
- **Prettier**: formatear código con `Shift + Alt + F`.
- **GitLens** (opcional).

**Seleccionar el intérprete de Python en VS Code:** `Ctrl + Shift + P` → "Python: Select Interpreter" → elige el que dice `('venv': venv)`.

---

## Parte 4. Entornos virtuales de Python (lo que más confunde)

### ¿Por qué?
Cada proyecto puede necesitar versiones distintas de librerías. El entorno virtual (`venv`) es una carpeta dentro del proyecto con su propio `pip` y sus propias librerías.

### Ciclo completo

```bash
cd ruta\del\proyecto
python -m venv venv                  # 1. crear (solo la primera vez)
venv\Scripts\activate                # 2. activar (CADA vez que abres una terminal)
                                     #    Linux/Mac: source venv/bin/activate
pip install -r requirements.txt      # 3. instalar dependencias (primera vez)
python app.py                        # 4. ejecutar
deactivate                           # 5. salir del entorno (opcional)
```

Sabes que está activo porque el prompt empieza con `(venv)`.

### Errores típicos

| Síntoma | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'flask'` | El venv no está activo, o no instalaste | `venv\Scripts\activate` y luego `pip install flask` |
| `venv\Scripts\activate : ... no está firmado digitalmente` | Política de PowerShell | `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y vuelve a activar |
| `pip` no se reconoce | pip no está en el PATH | `python -m pip install flask` |
| Instalé en otra terminal y "no está" | Cada terminal necesita activar el venv | Activa en esta terminal también |
| VS Code subraya `import flask` en amarillo | VS Code usa otro intérprete | `Ctrl+Shift+P` → Python: Select Interpreter → venv |

### Sin venv (si hay prisa)
Funciona instalar globalmente: `pip install flask`. En la prueba es aceptable; en el README menciona que se recomienda venv.

---

## Parte 5. Node y npm en detalle

```bash
npm init -y                    # crea package.json
npm install express            # dependencia → node_modules + package.json
npm install -D nodemon         # dependencia solo de desarrollo
npm install                    # instala TODO lo que dice package.json (tras clonar/descomprimir)
npm run dev                    # ejecuta el script "dev" de package.json
npm start                      # atajo de "npm run start"
npm test                       # atajo de "npm run test"
npx paquete                    # ejecuta un paquete sin instalarlo globalmente
node archivo.js                # ejecutar un archivo
node --watch archivo.js        # ejecutar y reiniciar al guardar (Node 18.11+)
```

- `node_modules/` **nunca** se copia ni se sube a Git. Se regenera con `npm install`.
- `package-lock.json` fija las versiones exactas. Sí se sube a Git.
- **`"type": "module"`** en package.json → usar `import`. Sin eso → `require`.

| Síntoma | Solución |
|---|---|
| `Cannot find module 'express'` | Falta `npm install` en la carpeta del proyecto |
| `Cannot use import statement outside a module` | Agrega `"type": "module"` a package.json |
| `EADDRINUSE :::3000` | Ya hay algo en el puerto 3000: cierra la otra terminal o cambia el puerto |
| `npm ERR! code ENOENT ... package.json` | No estás en la carpeta del proyecto (`cd`) |
| `gyp ERR!` al instalar | Paquete nativo sin binario para tu PC: usa una alternativa (ver Plan B en la guía de Express) |

**Matar el proceso de un puerto en Windows:**
```bash
netstat -ano | findstr :3000        # la última columna es el PID
taskkill /PID 12345 /F
```

---

## Parte 6. Java en detalle

```bash
javac Programa.java                 # compila → Programa.class
java Programa                       # ejecuta (SIN .class ni .java)
java Programa.java                  # Java 11+: compila y ejecuta en un paso (un solo archivo)
javac -encoding UTF-8 Programa.java # si hay tildes y ves caracteres raros
```

- El archivo debe llamarse **igual que la clase pública**: `public class Biblioteca` → `Biblioteca.java`.
- Si la consola muestra `?` en lugar de tildes: ejecuta `chcp 65001` antes.
- Con paquetes (`package com.ejemplo;`): compila desde la carpeta raíz: `javac com/ejemplo/Main.java` y luego `java com.ejemplo.Main`.
- En VS Code con el Extension Pack for Java aparece un botón **▶ Run** sobre `main`.
- NetBeans/IntelliJ/Eclipse: *File → New Project → Java Application*, pega el código y usa **Run** (F6 en NetBeans).

---

## Parte 7. Cómo ejecutar CADA programa del kit

> En todos los casos: primero descomprime el zip y abre una terminal **en la carpeta indicada**.

### 7.1 Cheatsheets (`01-cheatsheets/`)
Son archivos Markdown `.md`. Ábrelos en VS Code y presiona **`Ctrl + Shift + V`** para verlos formateados, o abre las versiones `.html` en el navegador.

### 7.2 Ejemplos ejecutables de los cheatsheets (`05-ejemplos/`)

| Carpeta | Comando | Requisitos |
|---|---|---|
| `05-ejemplos/python/` | `python 01_basicos.py` (cambia el número) | Solo Python |
| `05-ejemplos/javascript/` | `node 01_basicos.js` | Solo Node |
| `05-ejemplos/java/` | `java Basicos.java` | JDK 11+ |
| `05-ejemplos/php/` | `php basicos.php` (o `C:\xampp\php\php.exe basicos.php`) | PHP |
| `05-ejemplos/typescript/` | `npx tsx basicos.ts` (descarga tsx la primera vez) | Node + internet |
| `05-ejemplos/web-dom/index.html` | Doble clic → se abre en el navegador | Navegador |

Cada archivo imprime resultados comentados. Léelo **y** ejecútalo.

### 7.3 Proyecto Python Flask (`02-proyectos/python-flask-crud/`)
```bash
cd 02-proyectos\python-flask-crud
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
- Abre http://127.0.0.1:5000 → debes ver la tabla con Ana Pérez y Luis Mora.
- API: http://127.0.0.1:5000/api/estudiantes
- Pruebas: `python -m unittest -v` → `Ran 9 tests ... OK`
- Detener: `Ctrl + C`. Reiniciar datos: borra `instituto.db`.

### 7.4 Proyecto Node Express (`02-proyectos/node-express-crud/`)
```bash
cd 02-proyectos\node-express-crud
npm install
npm run dev
```
- http://localhost:3000 → inventario con 3 productos.
- Pruebas: `npm test` → `# pass 8`.
- Reiniciar datos: borra `db.json`.

### 7.5 Proyecto React (`02-proyectos/react-vite-crud/`)
Necesita **dos terminales** abiertas al mismo tiempo:
```bash
# Terminal 1 (backend)
cd 02-proyectos\node-express-crud
npm install
npm run dev

# Terminal 2 (frontend)
cd 02-proyectos\react-vite-crud
npm install
npm run dev
```
Abre http://localhost:5173. Si dice "No se pudo conectar con la API", la terminal 1 no está corriendo.

### 7.6 Proyecto Java (`02-proyectos/java-consola-poo/`)
```bash
cd 02-proyectos\java-consola-poo
chcp 65001
javac -encoding UTF-8 Biblioteca.java
java Biblioteca            # menú interactivo: escribe números y Enter
java Biblioteca --test     # pruebas
```

### 7.7 Ejercicios de lógica (`03-logica/`)
```bash
cd 03-logica
python soluciones.py             # 30 ejercicios originales
node soluciones.js
python soluciones_extra.py       # 20 ejercicios nuevos
node soluciones_extra.js
```
**Cómo practicar:** crea `mis_soluciones.py`, escribe tus funciones con los mismos nombres y al final agrega `from soluciones import *` **al inicio** para las que no hayas hecho. O copia el bloque de pruebas de `soluciones.py` debajo de tu código.

**Ejecutar una sola función de forma interactiva:**
```bash
python
>>> from soluciones import es_primo
>>> es_primo(97)
True
>>> exit()
```
En Node: `node` y luego `> const m = await import("./soluciones_extra.js")`.

### 7.8 SQL (`03-logica/sql/`)
Tres formas, de la más fácil a la más "real":

**A) Online, sin instalar nada:** https://sqliteonline.com → pega el contenido de `practica.sql` → *Run*.

**B) Con Python (SQLite viene incluido):**
```bash
cd 03-logica\sql
python ejecutar_sql.py practica.sql             # ejecuta y muestra cada resultado
python ejecutar_sql.py ejercicios_extra.sql
python ejecutar_sql.py                           # modo interactivo: escribe SQL y Enter
```

**C) Con MySQL (XAMPP):**
1. Start MySQL en XAMPP → http://localhost/phpmyadmin.
2. *Nueva* → crear base `practica` → pestaña **SQL**.
3. Pega `practica_mysql.sql` (versión adaptada a MySQL) → *Continuar*.

Desde la terminal: `C:\xampp\mysql\bin\mysql -u root practica < practica_mysql.sql`

**D) VS Code:** extensión *SQLite Viewer* → abre el `.db` para ver tablas.

### 7.9 Simulacro (`04-simulacro/`)
- Enunciado: `enunciado.md`.
- Plantillas de un archivo:
  ```bash
  cd 04-simulacro\plantillas
  pip install flask
  python flask_un_archivo.py        # http://127.0.0.1:5000

  npm init -y
  npm install express
  node express_un_archivo.js        # http://localhost:3000
  ```
- Solución:
  ```bash
  cd 04-simulacro\solucion-flask
  pip install flask
  python app.py                     # http://127.0.0.1:5000
  python -m unittest -v
  ```

### 7.10 Soluciones de los retos (`06-retos-resueltos/`)
Cada carpeta es una copia **extendida** del proyecto original, con los retos implementados. Se ejecuta **exactamente igual** que el proyecto original (secciones 7.3 a 7.6). En cada README está la lista de cambios y dónde encontrarlos.

---

## Parte 8. Probar APIs sin Postman

**Navegador:** solo sirve para GET → escribe la URL.

**PowerShell:**
```powershell
# GET
Invoke-RestMethod http://localhost:3000/api/productos
# POST
Invoke-RestMethod -Method Post -Uri http://localhost:3000/api/productos `
  -ContentType "application/json" `
  -Body '{"nombre":"Mouse","categoria":"PC","precio":10,"stock":5}'
# PUT
Invoke-RestMethod -Method Put -Uri http://localhost:3000/api/productos/1 -ContentType "application/json" -Body '{"stock":50}'
# DELETE
Invoke-RestMethod -Method Delete -Uri http://localhost:3000/api/productos/1
```
> En PowerShell, `curl` es un alias de `Invoke-WebRequest`. Para el curl real, escribe `curl.exe`.

**CMD / Git Bash / Linux (curl):**
```bash
curl http://localhost:3000/api/productos
curl -X POST http://localhost:3000/api/productos -H "Content-Type: application/json" -d "{\"nombre\":\"Mouse\",\"categoria\":\"PC\",\"precio\":10,\"stock\":5}"
curl -X DELETE http://localhost:3000/api/productos/1 -i      # -i muestra el código HTTP
```

**Thunder Client (VS Code):** icono del rayo → *New Request* → elige el método → URL → pestaña *Body* → *JSON* → *Send*.

**Desde la consola del navegador (F12 → Console):**
```js
await (await fetch("/api/productos", { method: "POST", headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ nombre: "Mouse", categoria: "PC", precio: 10, stock: 5 }) })).json()
```

---

## Parte 9. Depurar (encontrar errores) rápido

1. **Lee la ÚLTIMA línea del error**, que dice qué pasó. Las líneas de arriba dicen dónde (archivo y número de línea).
2. **print / console.log** de las variables sospechosas.
3. **F12 en el navegador:**
   - *Console*: errores de JavaScript.
   - *Network*: peticiones al servidor, su código (200/400/500) y su respuesta.
   - *Elements*: HTML real y estilos aplicados.
4. **Depurador de VS Code:** clic a la izquierda del número de línea (punto rojo = breakpoint) → `F5` → elige Python/Node → avanza con `F10`.
5. **Error 500 en Flask** con `debug=True`: la página muestra el traceback completo. En Express, mira la terminal donde corre el servidor.
6. Si algo "no cambia": ¿guardaste el archivo? ¿Reiniciaste el servidor? ¿Recargaste con `Ctrl + F5` (sin caché)?

---

## Parte 10. Checklist en el laboratorio (primeros 5 minutos)

1. Abrir una terminal y verificar versiones (Parte 3).
2. ¿Hay internet? → `pip install flask` o `npm install express` en una carpeta de prueba.
3. ¿Hay XAMPP? → Buscar `C:\xampp`. ¿MySQL arranca?
4. ¿Qué editor hay? (VS Code, NetBeans, Sublime...)
5. Configurar Git (`user.name`, `user.email`).
6. Crear la carpeta del proyecto en el **Escritorio**, no en rutas raras con espacios.

**Si no hay internet:** Python con `sqlite3`, `http.server`, `json` y `csv` funciona sin instalar nada. También PHP con XAMPP. Node sin paquetes (`http`, `fs`, `node:sqlite` en Node 22.5+). Tienes un ejemplo de servidor web sin librerías en `05-ejemplos/python/10_servidor_sin_flask.py` y `05-ejemplos/javascript/10_servidor_sin_express.js`.
