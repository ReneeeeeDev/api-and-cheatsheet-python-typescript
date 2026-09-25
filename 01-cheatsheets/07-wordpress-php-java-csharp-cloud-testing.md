# Cheatsheet: WordPress, Java/C#/.NET, PHP, Azure/Vercel, Testing/QA y preguntas de entrevista

## 1. WordPress (está en los requisitos)

**Instalar localmente con XAMPP:**
1. Iniciar Apache y MySQL en XAMPP.
2. phpMyAdmin (http://localhost/phpmyadmin) → crear base `wordpress`.
3. Descomprimir WordPress en `C:\xampp\htdocs\wordpress`.
4. Ir a http://localhost/wordpress → idioma → BD: `wordpress`, usuario `root`, contraseña vacía, host `localhost`.
5. Título del sitio, usuario admin → Instalar.

**Tareas típicas que pueden pedir:**
- Crear páginas (Páginas → Añadir) vs entradas (Entradas → Añadir; son del blog, con fecha y categoría).
- Menú: Apariencia → Menús (o Editor del sitio en temas de bloques).
- Instalar tema: Apariencia → Temas → Añadir.
- Plugins comunes: **Contact Form 7 / WPForms** (formularios), **Yoast SEO**, **Elementor** (maquetador), **WooCommerce** (tienda), **UpdraftPlus** (respaldos), **Wordfence** (seguridad).
- Ajustes → Enlaces permanentes → "Nombre de la entrada" (URLs amigables).
- Usuarios y roles: Administrador, Editor, Autor, Colaborador, Suscriptor.

**Código básico (functions.php del tema hijo):**
```php
<?php
// Shortcode: [saludo nombre="Ana"]
function mi_saludo($atts) {
  $a = shortcode_atts(['nombre' => 'visitante'], $atts);
  return "<p>Hola " . esc_html($a['nombre']) . "</p>";
}
add_shortcode('saludo', 'mi_saludo');

// Cargar CSS
add_action('wp_enqueue_scripts', function () {
  wp_enqueue_style('mi-estilo', get_stylesheet_directory_uri() . '/mi.css');
});
```
Conceptos: **hooks** (actions = hacer algo en un momento; filters = modificar un valor), **tema hijo** (para no perder cambios al actualizar), **The Loop** (`while (have_posts()) : the_post(); the_title(); endwhile;`).

## 2. PHP (el ISTE probablemente usa mucho PHP)

```php
<?php
$nombre = "Ana"; $edad = 25;
echo "Hola $nombre, tienes {$edad} años";
$nums = [5, 3, 8];  $persona = ["nombre" => "Ana", "edad" => 25];
foreach ($persona as $k => $v) { echo "$k: $v<br>"; }
count($nums); array_push($nums, 9); in_array(3, $nums); sort($nums);
$pares = array_filter($nums, fn($n) => $n % 2 == 0);
$dobles = array_map(fn($n) => $n * 2, $nums);
function sumar(int $a, int $b = 0): int { return $a + $b; }

// Formulario
if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $nombre = trim($_POST["nombre"] ?? "");
  if ($nombre === "") { $error = "Nombre obligatorio"; }
}
echo htmlspecialchars($nombre);   // evita XSS al imprimir

// PDO + MySQL (consultas preparadas)
$pdo = new PDO("mysql:host=localhost;dbname=tienda;charset=utf8mb4", "root", "",
               [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
$st = $pdo->prepare("INSERT INTO productos (nombre, precio) VALUES (?, ?)");
$st->execute([$nombre, $precio]);
$id = $pdo->lastInsertId();
$productos = $pdo->query("SELECT * FROM productos")->fetchAll(PDO::FETCH_ASSOC);
$st = $pdo->prepare("SELECT * FROM productos WHERE id = ?"); $st->execute([$id]); $p = $st->fetch();

// Clases
class Producto {
  public function __construct(public string $nombre, private float $precio) {}
  public function getPrecio(): float { return $this->precio; }
}
header("Location: index.php"); exit;   // redirigir
session_start(); $_SESSION["usuario"] = "ana";
```

## 3. Java (sintaxis rápida)

```java
import java.util.*;
import java.util.stream.*;

public class Main {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int n = sc.nextInt(); sc.nextLine();
    String nombre = sc.nextLine();
    System.out.printf("Hola %s, número %d%n", nombre, n);

    List<Integer> nums = new ArrayList<>(List.of(5, 3, 8, 1));
    Collections.sort(nums);
    List<Integer> pares = nums.stream().filter(x -> x % 2 == 0).collect(Collectors.toList());
    int suma = nums.stream().mapToInt(Integer::intValue).sum();

    Map<String, Integer> mapa = new HashMap<>();
    mapa.put("Ana", 9);  mapa.getOrDefault("Luis", 0);
    for (Map.Entry<String, Integer> e : mapa.entrySet()) System.out.println(e.getKey());

    String s = "Hola"; s.length(); s.charAt(0); s.toUpperCase(); s.equals("Hola"); // ¡equals, no ==!
    new StringBuilder(s).reverse().toString();
    int[] arr = {3, 1, 2}; Arrays.sort(arr); System.out.println(Arrays.toString(arr));
  }
}
// Compilar y ejecutar: javac Main.java && java Main
```

## 4. C# / .NET (familiaridad)

```csharp
var nombre = "Ana"; int edad = 25;
Console.WriteLine($"Hola {nombre}, {edad} años");
var nums = new List<int> { 5, 3, 8 };
var pares = nums.Where(n => n % 2 == 0).ToList();          // LINQ
var total = nums.Sum(); var max = nums.Max();
var ordenados = nums.OrderByDescending(n => n).ToList();

public class Producto {
    public int Id { get; set; }
    public string Nombre { get; set; } = "";
    public decimal Precio { get; set; }
}
```

Comandos .NET:
```bash
dotnet new console -n MiApp       # app de consola
dotnet new webapi -n MiApi        # API REST
dotnet new mvc -n MiWeb           # MVC con vistas
dotnet run
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
```

Minimal API (.NET 8):
```csharp
var app = WebApplication.CreateBuilder(args).Build();
var productos = new List<Producto>();
app.MapGet("/api/productos", () => productos);
app.MapPost("/api/productos", (Producto p) => { productos.Add(p); return Results.Created($"/api/productos/{p.Id}", p); });
app.Run();
```

**Entity Framework Core**: ORM de .NET. `DbContext` con `DbSet<Producto>`; migraciones con `dotnet ef migrations add Inicial` y `dotnet ef database update`.

## 5. Azure y Vercel (nociones)

**Vercel**: hosting para frontend y Next.js. Conectas el repo de GitHub, cada push a `main` despliega a producción y cada rama/PR genera una URL de preview. Soporta funciones serverless (`/api`). Variables de entorno en el panel.

**Azure** (nube de Microsoft):
- **App Service**: hosting de apps web (.NET, Node, Python, PHP).
- **Azure SQL Database**: SQL Server administrado.
- **Storage Account (Blob)**: archivos/imagenes.
- **Azure Functions**: serverless.
- **Static Web Apps**: frontends estáticos (React) con API.
- **Azure DevOps / GitHub Actions**: CI/CD.
- **Resource Group**: contenedor lógico de recursos.

Conceptos cloud: **IaaS** (máquinas virtuales), **PaaS** (App Service, sin gestionar servidor), **SaaS** (Office 365), **serverless** (pagas por ejecución), **CI/CD** (integración y despliegue continuo automatizado).

## 6. Testing / QA

- **Unitarias**: prueban una función aislada (unittest, pytest, Jest, JUnit, xUnit).
- **Integración**: prueban varias piezas juntas (API + BD).
- **End-to-end (E2E)**: simulan al usuario en el navegador (Cypress, Playwright, Selenium).
- **Funcionales / aceptación**: verifican requisitos del negocio.
- **Regresión**: re-ejecutar pruebas para confirmar que nada se rompió.
- **Caja negra** (sin ver el código, entradas/salidas) vs **caja blanca** (conociendo el código).
- **TDD**: escribir la prueba primero, luego el código (Red → Green → Refactor).
- **Casos de prueba**: ID, descripción, precondiciones, pasos, datos, resultado esperado, resultado obtenido, estado.
- Probar siempre: caso normal, **valores límite** (0, vacío, máximo), datos inválidos, duplicados.
- Probar APIs: Postman / Thunder Client / `curl`:
  ```bash
  curl http://localhost:3000/api/productos
  curl -X POST http://localhost:3000/api/productos -H "Content-Type: application/json" -d "{\"nombre\":\"Mouse\",\"precio\":10}"
  ```

Ejemplo de caso de prueba:

| ID | Caso | Datos | Esperado |
|---|---|---|---|
| CP-01 | Crear producto válido | nombre=Mouse, precio=10 | 201, aparece en la lista |
| CP-02 | Nombre vacío | nombre="", precio=10 | 400, mensaje "nombre obligatorio" |
| CP-03 | Precio negativo | precio=-5 | 400 |
| CP-04 | Eliminar inexistente | id=999 | 404 |

## 7. Preguntas de entrevista técnica (respuestas cortas)

- **¿Qué es una API REST?** Interfaz que expone recursos por HTTP usando verbos: GET (leer), POST (crear), PUT/PATCH (actualizar total/parcial), DELETE (eliminar). Sin estado, normalmente en JSON.
- **MVC**: Modelo (datos y lógica), Vista (interfaz), Controlador (recibe peticiones y coordina).
- **Frontend vs Backend**: lo que corre en el navegador vs lo que corre en el servidor.
- **Cookies vs sesión vs JWT**: cookie se guarda en el navegador; la sesión guarda datos en el servidor identificados por una cookie; JWT es un token firmado que el cliente envía en cada petición.
- **Autenticación vs autorización**: quién eres vs qué puedes hacer.
- **Hash de contraseñas**: nunca guardar en texto plano; usar bcrypt/argon2 (`password_hash` en PHP).
- **OWASP top**: SQL Injection, XSS, CSRF, autenticación rota, datos sensibles expuestos.
- **SOLID**: Responsabilidad única, Abierto/cerrado, Sustitución de Liskov, Segregación de interfaces, Inversión de dependencias.
- **Big O**: O(1) constante, O(log n) búsqueda binaria, O(n) recorrer, O(n log n) buen ordenamiento, O(n²) doble bucle.
- **Pila vs cola**: LIFO vs FIFO.
- **Scrum**: sprints de 1–4 semanas, daily, sprint planning, review, retrospectiva; roles: Product Owner, Scrum Master, equipo.
- **¿Por qué quieres trabajar aquí?** Menciona crecer en un entorno educativo, contribuir a sistemas que usan estudiantes y docentes, y que el stack del puesto coincide con lo que dominas.
- **¿Un error que cometiste?** Uno real y pequeño, cómo lo detectaste y qué cambiaste (p. ej., ahora haces commits y pruebas antes de desplegar).
