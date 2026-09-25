# Cheatsheet: Dart/Flutter, WordPress a fondo, Azure y Vercel paso a paso

---

## PARTE A — Dart (y Flutter en lo básico)

### Ejecutar
- Instalar el Flutter SDK (incluye Dart) desde https://docs.flutter.dev/get-started/install, o solo Dart SDK.
- Sin instalar nada: **https://dartpad.dev** (online).
```bash
dart --version
dart run archivo.dart            # ejecutar un script
dart create -t console mi_app    # proyecto de consola
flutter create mi_app && cd mi_app && flutter run    # app móvil/web/escritorio
flutter doctor                   # diagnóstico del entorno
```

### Sintaxis
```dart
void main() {
  // Variables
  var nombre = 'Ana';            // inferido
  String ciudad = 'Ambato';
  int edad = 25; double nota = 8.5; bool activo = true;
  final creado = DateTime.now(); // se asigna una vez (en ejecución)
  const iva = 0.15;              // constante en compilación
  String? email;                 // null safety: ? = puede ser null
  print('Hola $nombre, ${edad + 1} años. Email: ${email ?? "sin email"}');

  // Listas, mapas y sets
  final nums = [5, 3, 8, 1];
  nums.add(10);
  final pares = nums.where((n) => n.isEven).toList();
  final dobles = nums.map((n) => n * 2).toList();
  final total = nums.reduce((a, b) => a + b);
  nums.sort((a, b) => b.compareTo(a));
  final persona = {'nombre': 'Ana', 'edad': 25};   // Map<String, Object>
  final unicos = {1, 2, 2, 3};                     // Set
  print('$pares $dobles $total $nums ${persona['nombre']} $unicos');

  // Control de flujo
  final estado = nota >= 7 ? 'Aprobado' : 'Reprobado';
  for (final n in nums) { if (n > 5) break; }
  switch (edad) { case < 18: print('Menor'); default: print('Mayor'); }   // Dart 3

  // Funciones
  print(sumar(2, 3));
  print(saludar('Luis', saludo: 'Buenas'));
  final doble = (int x) => x * 2;

  // POO
  final d = Docente('María', 1100, ['POO', 'BD']);
  print(d);
}

int sumar(int a, int b) => a + b;
String saludar(String nombre, {String saludo = 'Hola'}) => '$saludo, $nombre';   // parámetro con nombre

abstract class Empleado {
  final String nombre;
  Empleado(this.nombre);                 // atajo para asignar
  double calcularSueldo();
  @override
  String toString() => '$nombre: \$${calcularSueldo().toStringAsFixed(2)}';
}

class Docente extends Empleado {
  final double base;
  final List<String> materias;
  Docente(super.nombre, this.base, this.materias);
  @override
  double calcularSueldo() => base + 25 * materias.length;
}
```

### Async en Dart
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;    // dart pub add http

Future<List<dynamic>> cargarUsuarios() async {
  final r = await http.get(Uri.parse('https://jsonplaceholder.typicode.com/users'));
  if (r.statusCode != 200) throw Exception('Error ${r.statusCode}');
  return jsonDecode(r.body) as List<dynamic>;
}
```

### Flutter mínimo (contador + lista)
```dart
import 'package:flutter/material.dart';

void main() => runApp(const MaterialApp(home: Tareas()));

class Tareas extends StatefulWidget {
  const Tareas({super.key});
  @override
  State<Tareas> createState() => _TareasState();
}

class _TareasState extends State<Tareas> {
  final _items = <String>[];
  final _ctrl = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Tareas')),
      body: Column(children: [
        Padding(
          padding: const EdgeInsets.all(8),
          child: Row(children: [
            Expanded(child: TextField(controller: _ctrl, decoration: const InputDecoration(labelText: 'Nueva tarea'))),
            IconButton(icon: const Icon(Icons.add), onPressed: () {
              if (_ctrl.text.trim().isEmpty) return;
              setState(() => _items.add(_ctrl.text.trim()));   // setState redibuja
              _ctrl.clear();
            }),
          ]),
        ),
        Expanded(
          child: ListView.builder(
            itemCount: _items.length,
            itemBuilder: (_, i) => ListTile(
              title: Text(_items[i]),
              trailing: IconButton(icon: const Icon(Icons.delete), onPressed: () => setState(() => _items.removeAt(i))),
            ),
          ),
        ),
      ]),
    );
  }
}
```
Conceptos: todo es un **Widget**. `StatelessWidget` (sin estado) vs `StatefulWidget` (con estado y `setState`). Layout con `Column`, `Row`, `Expanded`, `Padding`, `Container`, `ListView`. Navegación: `Navigator.push(context, MaterialPageRoute(builder: (_) => Detalle()))`.

---

## PARTE B — WordPress a fondo

### Instalación local con XAMPP (paso a paso)
1. XAMPP → Start **Apache** y **MySQL**.
2. http://localhost/phpmyadmin → *Nueva* → base `wp_iste` → cotejamiento `utf8mb4_unicode_ci` → Crear.
3. Descarga https://es.wordpress.org/download/ y descomprime en `C:\xampp\htdocs\wp-iste\`.
4. http://localhost/wp-iste → idioma → datos de la base: nombre `wp_iste`, usuario `root`, contraseña (vacía), servidor `localhost`, prefijo `wp_`.
5. Título, usuario administrador (¡anota la contraseña!), email → Instalar.
6. Panel: http://localhost/wp-iste/wp-admin

### Tareas típicas en una prueba
| Tarea | Dónde |
|---|---|
| Crear página "Nosotros" | Páginas → Añadir nueva → editor de bloques (Gutenberg) → Publicar |
| Crear entrada de blog con categoría | Entradas → Añadir → panel derecho: Categorías, Etiquetas, Imagen destacada |
| Página de inicio estática | Ajustes → Lectura → "Una página estática" → Portada: Inicio, Entradas: Blog |
| URLs amigables | Ajustes → Enlaces permanentes → "Nombre de la entrada" |
| Menú | Apariencia → Menús (temas clásicos) o Apariencia → Editor → Navegación (temas de bloques) |
| Instalar tema | Apariencia → Temas → Añadir nuevo (Astra, Kadence, GeneratePress, Twenty Twenty-Five) |
| Formulario de contacto | Plugins → Añadir → **Contact Form 7** → copiar el shortcode `[contact-form-7 id="..."]` en una página |
| Tienda | Plugin **WooCommerce** → asistente → Productos → Añadir |
| SEO | **Yoast SEO** o **Rank Math** |
| Copias de seguridad | **UpdraftPlus** |
| Seguridad | **Wordfence**, limitar intentos de login, usuarios con contraseñas fuertes |
| Caché y velocidad | **LiteSpeed Cache** / **WP Super Cache**, optimizar imágenes con **Smush** |
| Usuarios | Usuarios → Añadir → rol (Administrador, Editor, Autor, Colaborador, Suscriptor) |
| Constructor visual | **Elementor** |
| Migrar un sitio | Plugin **All-in-One WP Migration** o **Duplicator** |

### Estructura de archivos
```
wp-iste/
├── wp-config.php          ← credenciales de BD, claves, WP_DEBUG
├── wp-content/
│   ├── themes/            ← temas (NUNCA edites el tema padre: usa un tema hijo)
│   ├── plugins/
│   └── uploads/           ← imágenes subidas
├── wp-admin/  wp-includes/   ← núcleo (no tocar)
```
Tablas principales: `wp_posts` (entradas, páginas, adjuntos, menús), `wp_postmeta`, `wp_users`, `wp_usermeta`, `wp_options` (configuración, `siteurl`, `home`), `wp_terms` / `wp_term_taxonomy` (categorías, etiquetas), `wp_comments`.

Activar la depuración en `wp-config.php`:
```php
define('WP_DEBUG', true);
define('WP_DEBUG_LOG', true);        // escribe en wp-content/debug.log
define('WP_DEBUG_DISPLAY', false);
```

### Tema hijo (child theme)
`wp-content/themes/astra-hijo/style.css`:
```css
/*
Theme Name: Astra Hijo
Template: astra
*/
```
`wp-content/themes/astra-hijo/functions.php`:
```php
<?php
add_action('wp_enqueue_scripts', function () {
    wp_enqueue_style('padre', get_template_directory_uri() . '/style.css');
    wp_enqueue_style('hijo', get_stylesheet_uri(), ['padre']);
});
```
Apariencia → Temas → activar "Astra Hijo".

### Hooks: actions y filters
```php
// ACTION: hacer algo en un momento determinado
add_action('wp_footer', function () {
    echo '<p style="text-align:center">© ' . date('Y') . ' ISTE</p>';
});

// FILTER: modificar un valor y devolverlo
add_filter('the_title', function ($titulo) {
    return is_single() ? '📘 ' . $titulo : $titulo;
});
add_filter('excerpt_length', fn() => 20);
```

### Shortcode, Custom Post Type y consulta
```php
// [cursos cantidad="3"]
add_shortcode('cursos', function ($atts) {
    $a = shortcode_atts(['cantidad' => 5], $atts);
    $q = new WP_Query(['post_type' => 'curso', 'posts_per_page' => (int)$a['cantidad']]);
    $html = '<ul>';
    while ($q->have_posts()) { $q->the_post(); $html .= '<li><a href="' . get_permalink() . '">' . esc_html(get_the_title()) . '</a></li>'; }
    wp_reset_postdata();
    return $html . '</ul>';
});

// Custom Post Type "Curso"
add_action('init', function () {
    register_post_type('curso', [
        'labels' => ['name' => 'Cursos', 'singular_name' => 'Curso'],
        'public' => true, 'has_archive' => true, 'menu_icon' => 'dashicons-welcome-learn-more',
        'supports' => ['title', 'editor', 'thumbnail'], 'show_in_rest' => true,
    ]);
});
```
Tras registrar un CPT: Ajustes → Enlaces permanentes → **Guardar**, para refrescar las URLs.

### Plugin mínimo propio
`wp-content/plugins/mi-aviso/mi-aviso.php`:
```php
<?php
/**
 * Plugin Name: Mi Aviso
 * Description: Muestra un aviso al inicio de cada entrada.
 * Version: 1.0
 */
if (!defined('ABSPATH')) exit;           // seguridad: no ejecutar directamente
add_filter('the_content', function ($contenido) {
    if (!is_single()) return $contenido;
    return '<div class="aviso">Inscripciones abiertas</div>' . $contenido;
});
```
Plugins → activar "Mi Aviso".

### The Loop (plantillas de tema)
```php
<?php if (have_posts()) : while (have_posts()) : the_post(); ?>
  <article>
    <h2><a href="<?php the_permalink(); ?>"><?php the_title(); ?></a></h2>
    <?php the_post_thumbnail('medium'); ?>
    <?php the_excerpt(); ?>
  </article>
<?php endwhile; else : ?>
  <p>No hay entradas.</p>
<?php endif; ?>
```
Jerarquía de plantillas: `single-curso.php` → `single.php` → `index.php`, y `page-nosotros.php` → `page.php` → `index.php`.

Funciones de seguridad: `esc_html()`, `esc_attr()`, `esc_url()`, `sanitize_text_field()`, `wp_nonce_field()` / `wp_verify_nonce()`, `current_user_can('edit_posts')`.

**API REST de WordPress:** `http://localhost/wp-iste/wp-json/wp/v2/posts`, `/pages`, `/users`, `/curso` (si el CPT tiene `show_in_rest`).

### Mantenimiento y seguridad (preguntas típicas)
- Actualizar núcleo, temas y plugins (con respaldo previo).
- Eliminar plugins y temas que no se usan.
- No usar el usuario "admin"; contraseñas fuertes y 2FA.
- Certificado SSL (https) y copias de seguridad automáticas.
- Si aparece "pantalla blanca de la muerte": activar WP_DEBUG, desactivar plugins renombrando la carpeta `plugins`, cambiar a un tema por defecto.
- "Error al establecer una conexión con la base de datos": revisar los datos de `wp-config.php` y que MySQL esté iniciado.

---

## PARTE C — Vercel paso a paso

1. Sube el proyecto a GitHub.
2. https://vercel.com → *Sign up with GitHub*.
3. **Add New → Project** → *Import* el repositorio.
4. Vercel detecta el framework (Next.js, Vite/React, estático). Revisa:
   - Build Command: `npm run build`
   - Output Directory: `dist` (Vite) o automático (Next).
5. **Environment Variables** (si hace falta, por ejemplo `VITE_API_URL`).
6. **Deploy** → URL tipo `https://mi-app.vercel.app`.
7. Cada `git push` a `main` redespliega a producción; cada rama o Pull Request genera una **Preview URL**.

CLI: `npm i -g vercel` → `vercel` (preview) → `vercel --prod`.

API serverless en Vercel (sin Next):
```js
// api/hola.js
export default function handler(req, res) {
  res.status(200).json({ mensaje: "Hola desde Vercel", metodo: req.method });
}
```
En React con Vite, si usas React Router añade `vercel.json` con `{"rewrites":[{"source":"/(.*)","destination":"/"}]}` para que al refrescar no dé 404.

---

## PARTE D — Azure paso a paso

### Conceptos
- **Suscripción** → **Grupo de recursos** (carpeta lógica) → **Recursos** (App Service, BD, Storage...).
- **Región:** dónde está físicamente (ej. East US, Brazil South).
- **IaaS** (Virtual Machines) vs **PaaS** (App Service, Azure SQL) vs **SaaS** (Microsoft 365) vs **Serverless** (Azure Functions).

### Servicios más comunes

| Servicio | Para qué | Equivalente AWS |
|---|---|---|
| App Service | Hospedar web/API (.NET, Node, Python, PHP, Java) | Elastic Beanstalk |
| Static Web Apps | Frontend estático (React) + API | Amplify / S3 |
| Azure Functions | Código serverless por eventos | Lambda |
| Azure SQL Database | SQL Server administrado | RDS |
| Azure Database for MySQL/PostgreSQL | MySQL/Postgres administrados | RDS |
| Cosmos DB | NoSQL | DynamoDB |
| Storage Account (Blob) | Archivos e imágenes | S3 |
| Key Vault | Secretos y contraseñas | Secrets Manager |
| Entra ID (antes Azure AD) | Identidad y login | IAM / Cognito |
| Virtual Machines | Servidores completos | EC2 |
| Azure DevOps / GitHub Actions | CI/CD | CodePipeline |
| Application Insights | Monitoreo y logs | CloudWatch |

### Desplegar una app Node/Python en App Service (portal)
1. https://portal.azure.com → **Crear un recurso** → **Aplicación web**.
2. Grupo de recursos: nuevo `rg-iste`. Nombre: `reservas-iste` (será `reservas-iste.azurewebsites.net`).
3. Pila del entorno: Node 22 LTS / Python 3.12. SO: Linux. Plan: **Free F1** (para pruebas).
4. Crear → ir al recurso → **Centro de implementación** → Origen: **GitHub** → repositorio y rama → Guardar (crea un GitHub Action que despliega en cada push).
5. **Configuración → Variables de entorno**: `PORT`, cadenas de conexión, etc.
6. Para Python/Flask: Configuración → Comando de inicio: `gunicorn --bind=0.0.0.0 --timeout 600 app:app` (y agrega `gunicorn` a requirements.txt).

### Azure CLI (alternativa)
```bash
az login
az group create -n rg-iste -l eastus
az webapp up --name reservas-iste --runtime "NODE:22-lts" --sku F1     # desde la carpeta del proyecto
az webapp log tail --name reservas-iste --resource-group rg-iste
```

### Azure SQL
Crear recurso **SQL Database** → servidor nuevo (usuario/contraseña) → Redes: "Permitir que servicios de Azure accedan" y agregar tu IP → la cadena de conexión está en *Cadenas de conexión*.

---

## PARTE E — Testing / QA ampliado

### Pirámide de pruebas
```
        /  E2E  \        pocas: lentas, prueban el flujo completo en el navegador (Playwright, Cypress, Selenium)
       / Integración \   varias: API + BD (Supertest, Flask test_client)
      /   Unitarias    \ muchas: funciones puras, rápidas (unittest, pytest, Jest, JUnit, xUnit)
```

### Técnicas de diseño de casos de prueba
- **Partición de equivalencia:** dividir las entradas en grupos que se comportan igual (nota: <0 inválida, 0–6.99 reprueba, 7–10 aprueba, >10 inválida) y probar un valor de cada grupo.
- **Valores límite:** probar en los bordes: -0.01, 0, 6.99, 7, 10, 10.01.
- **Tabla de decisión:** combinaciones de condiciones (laboratorio disponible × horario libre × horas válidas).
- **Transición de estados:** ticket abierto → en proceso → cerrado (probar transiciones válidas e inválidas).
- **Pruebas negativas:** datos vacíos, tipos incorrectos, duplicados, IDs inexistentes, textos muy largos, caracteres especiales (`<script>`, `' OR 1=1`).

### Plantilla de caso de prueba
| Campo | Ejemplo |
|---|---|
| ID | CP-RES-003 |
| Módulo | Reservas |
| Descripción | Rechazar reserva que se cruza con otra existente |
| Precondición | Existe reserva LAB-002, 25/09/2026, 08:00–10:00 |
| Pasos | 1. Ir a Reservas 2. Llenar LAB-002, 25/09/2026, 09:00–11:00 3. Clic en Reservar |
| Datos | docente "Ing. Ruiz" |
| Resultado esperado | Mensaje "Horario ocupado", la reserva no se guarda, HTTP 400 |
| Resultado obtenido | (se llena al ejecutar) |
| Estado | Aprobado / Fallido |
| Severidad / Prioridad | Alta / Alta |

### Reporte de bug (defecto)
**Título:** "Se permite reservar un laboratorio en mantenimiento" · **Pasos para reproducir** · **Resultado esperado vs obtenido** · **Entorno** (Windows 11, Chrome 129, versión 1.2) · **Evidencia** (captura) · **Severidad** (Crítica / Mayor / Menor / Trivial) · **Prioridad**.

### E2E con Playwright (ejemplo)
```bash
npm init playwright@latest
npx playwright test          npx playwright codegen http://localhost:3000   # graba tus clics y genera el código
```
```js
import { test, expect } from "@playwright/test";
test("crear reserva y detectar choque", async ({ page }) => {
  await page.goto("http://localhost:3000/reservas");
  await page.fill("[name=docente]", "Ing. Ruiz");
  await page.selectOption("[name=laboratorio_id]", "2");
  await page.fill("[name=fecha]", "2026-09-25");
  await page.fill("[name=hora_inicio]", "08:00");
  await page.fill("[name=hora_fin]", "10:00");
  await page.click("text=Reservar");
  await expect(page.locator(".alerta.ok")).toContainText("Reserva registrada");
});
```

### Otros términos de QA
- **Smoke test:** prueba rápida de que lo principal funciona tras un despliegue.
- **Sanity test:** prueba enfocada de un arreglo puntual.
- **Regresión:** volver a probar para confirmar que nada se rompió.
- **UAT:** prueba de aceptación por parte del usuario final.
- **Cobertura:** % de código ejecutado por las pruebas (`coverage run -m unittest`, `npx jest --coverage`).
- **Mock / stub:** objeto falso que reemplaza una dependencia (BD, API externa).
- **Pruebas de carga:** JMeter, k6. **Seguridad:** OWASP ZAP.
- **Verificación vs validación:** ¿lo construimos bien? (según la especificación) vs ¿construimos lo correcto? (lo que necesita el usuario).
