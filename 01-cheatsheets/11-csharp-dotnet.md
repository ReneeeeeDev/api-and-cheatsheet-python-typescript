# Cheatsheet C# y .NET (la oferta pide "familiaridad con .NET")

## 1. Instalar y ejecutar

- Instalar el **.NET SDK 8 o 9**: https://dotnet.microsoft.com/download → `dotnet --version`.
- IDE: **Visual Studio 2022 Community** (Windows) o **VS Code + C# Dev Kit**.

```bash
dotnet new console -n Calculadora         # app de consola
cd Calculadora
dotnet run                                # compila y ejecuta
dotnet new webapi -n ApiTienda            # API REST
dotnet new mvc -n WebTienda               # MVC con vistas Razor
dotnet new blazor -n AppBlazor            # UI con C# en el navegador
dotnet new xunit -n Pruebas               # proyecto de pruebas
dotnet add package Microsoft.EntityFrameworkCore.Sqlite
dotnet build        dotnet test        dotnet watch run (recarga al guardar)
dotnet publish -c Release
```
En Visual Studio: *Crear proyecto* → "Aplicación de consola" o "ASP.NET Core Web API" → `F5` (con depuración) o `Ctrl+F5` (sin depuración).

## 2. Sintaxis básica

```csharp
// Program.cs con "top-level statements" (.NET 6+): no hace falta la clase Main
using System.Linq;

string nombre = "Ana";
int edad = 25;
double nota = 8.5;
decimal precio = 12.50m;          // decimal para dinero (sufijo m)
bool activo = true;
var inferido = 10;                // tipo inferido
const double IVA = 0.15;
string? email = null;             // tipo que acepta null (nullable)

Console.WriteLine($"Hola {nombre}, tienes {edad} años. Precio: {precio:C2} {nota:F1}");
Console.Write("Número: ");
int n = int.Parse(Console.ReadLine() ?? "0");
if (int.TryParse("abc", out int valor)) { } else { Console.WriteLine("No es número"); }

string estado = nota >= 7 ? "Aprobado" : "Reprobado";
string dia = n switch { 1 or 7 => "Fin de semana", >= 2 and <= 6 => "Laborable", _ => "Inválido" };
for (int i = 0; i < 3; i++) { }
foreach (var x in lista) { }
while (n > 0) n--;

// Strings
nombre.ToUpper(); nombre.Length; nombre.Contains("A"); nombre.Substring(0, 2); nombre.Replace("a", "o");
string.Join(",", lista); "a,b".Split(','); nombre.Trim(); string.IsNullOrWhiteSpace(email);
```

## 3. Colecciones y LINQ (lo más característico de C#)

```csharp
var nums = new List<int> { 5, 3, 8, 1 };
nums.Add(10); nums.Remove(3); nums.Contains(8); nums.Count; nums.Sort();
var dic = new Dictionary<string, int> { ["mouse"] = 10, ["teclado"] = 3 };
dic["monitor"] = 2; dic.TryGetValue("mouse", out int stock); dic.ContainsKey("x");
var conjunto = new HashSet<int> { 1, 2, 2 };
int[] arreglo = { 1, 2, 3 }; int[,] matriz = new int[2, 3];

// LINQ (sintaxis de métodos)
var pares = nums.Where(x => x % 2 == 0).ToList();
var dobles = nums.Select(x => x * 2);
var total = nums.Sum(); var prom = nums.Average(); var max = nums.Max();
var primero = nums.FirstOrDefault(x => x > 4);        // 0/null si no hay
bool alguno = nums.Any(x => x > 7); bool todos = nums.All(x => x > 0);
var ordenados = estudiantes.OrderByDescending(e => e.Nota).ThenBy(e => e.Nombre).ToList();
var porCarrera = estudiantes.GroupBy(e => e.Carrera)
                            .Select(g => new { Carrera = g.Key, Cantidad = g.Count(), Promedio = g.Average(e => e.Nota) });
var pagina = lista.Skip(10).Take(10);
var unicos = nums.Distinct();
// Sintaxis de consulta (parecida a SQL)
var consulta = from e in estudiantes where e.Nota >= 7 orderby e.Nombre select e.Nombre;
```

## 4. POO en C#

```csharp
public interface IPagable { decimal CalcularPago(); }

public abstract class Empleado : IPagable
{
    private static int _contador;
    public int Id { get; }                              // propiedad de solo lectura
    public string Nombre { get; set; }                  // propiedad auto-implementada
    protected Empleado(string nombre) { Id = ++_contador; Nombre = nombre; }
    public abstract decimal CalcularPago();
    public decimal AporteIess() => Math.Round(CalcularPago() * 0.0945m, 2);   // expression-bodied
    public override string ToString() => $"#{Id} {Nombre}: {CalcularPago():C}";
}

public class Docente : Empleado
{
    private decimal _sueldo;
    public decimal Sueldo
    {
        get => _sueldo;
        set => _sueldo = value >= 0 ? value : throw new ArgumentException("Sueldo inválido");
    }
    public List<string> Materias { get; init; } = new();    // init: solo al crear
    public Docente(string nombre, decimal sueldo) : base(nombre) { Sueldo = sueldo; }
    public override decimal CalcularPago() => Sueldo + 25 * Materias.Count;
}

var d = new Docente("María", 1100) { Materias = ["POO", "BD"] };
Console.WriteLine(d);

public record Producto(int Id, string Nombre, decimal Precio);   // inmutable, con igualdad por valor
var p2 = p1 with { Precio = 20 };                                // copia modificada
```
Modificadores: `public`, `private`, `protected`, `internal` (mismo proyecto), `static`, `readonly`, `sealed` (no heredable), `virtual`/`override`, `abstract`.

## 5. Excepciones y async

```csharp
try { var r = 10 / cero; }
catch (DivideByZeroException ex) { Console.WriteLine(ex.Message); }
catch (Exception ex) when (ex is ArgumentException) { }
finally { }
throw new InvalidOperationException("Stock insuficiente");
public class StockException(string msg) : Exception(msg);         // C# 12: constructor primario

public async Task<List<Usuario>> CargarAsync()
{
    using var http = new HttpClient();
    var usuarios = await http.GetFromJsonAsync<List<Usuario>>("https://jsonplaceholder.typicode.com/users");
    return usuarios ?? [];
}
```

## 6. ASP.NET Core Minimal API (API REST completa)

```csharp
// Program.cs  (dotnet new web -n Api; dotnet add package Microsoft.EntityFrameworkCore.Sqlite)
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<TiendaDb>(o => o.UseSqlite("Data Source=tienda.db"));
builder.Services.AddCors(o => o.AddDefaultPolicy(p => p.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()));
var app = builder.Build();
app.UseCors();

using (var scope = app.Services.CreateScope())
    scope.ServiceProvider.GetRequiredService<TiendaDb>().Database.EnsureCreated();

var api = app.MapGroup("/api/productos");
api.MapGet("/", async (TiendaDb db, string? q) =>
    await db.Productos.Where(p => q == null || p.Nombre.Contains(q)).OrderBy(p => p.Nombre).ToListAsync());
api.MapGet("/{id:int}", async (int id, TiendaDb db) =>
    await db.Productos.FindAsync(id) is Producto p ? Results.Ok(p) : Results.NotFound());
api.MapPost("/", async (Producto p, TiendaDb db) =>
{
    if (string.IsNullOrWhiteSpace(p.Nombre) || p.Precio <= 0) return Results.BadRequest(new { error = "Datos inválidos" });
    db.Productos.Add(p);
    await db.SaveChangesAsync();
    return Results.Created($"/api/productos/{p.Id}", p);
});
api.MapPut("/{id:int}", async (int id, Producto datos, TiendaDb db) =>
{
    var p = await db.Productos.FindAsync(id);
    if (p is null) return Results.NotFound();
    p.Nombre = datos.Nombre; p.Precio = datos.Precio;
    await db.SaveChangesAsync();
    return Results.Ok(p);
});
api.MapDelete("/{id:int}", async (int id, TiendaDb db) =>
{
    var p = await db.Productos.FindAsync(id);
    if (p is null) return Results.NotFound();
    db.Productos.Remove(p); await db.SaveChangesAsync();
    return Results.NoContent();
});
app.Run();

public class Producto { public int Id { get; set; } public string Nombre { get; set; } = ""; public decimal Precio { get; set; } }
public class TiendaDb(DbContextOptions<TiendaDb> o) : DbContext(o) { public DbSet<Producto> Productos => Set<Producto>(); }
```
`dotnet run` → http://localhost:5xxx/api/productos (el puerto aparece en la consola). Con la plantilla `webapi` tienes Swagger/OpenAPI para probar desde el navegador.

## 7. Entity Framework Core (ORM)

```bash
dotnet tool install --global dotnet-ef
dotnet add package Microsoft.EntityFrameworkCore.SqlServer    # o .Sqlite / Pomelo.EntityFrameworkCore.MySql
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet ef migrations add Inicial
dotnet ef database update
```
```csharp
db.Productos.Add(p); db.SaveChanges();
db.Productos.Find(1); db.Productos.Where(p => p.Precio > 10).ToList();
db.Estudiantes.Include(e => e.Carrera).ToList();     // JOIN (carga la relación)
db.Productos.Remove(p); db.SaveChanges();
```
Cadena de conexión SQL Server: `"Server=localhost;Database=Tienda;Trusted_Connection=True;TrustServerCertificate=True"`.

## 8. MVC con Razor (vistas)

`dotnet new mvc` → `Controllers/HomeController.cs`, `Views/Home/Index.cshtml`, `Models/`.
```csharp
public class ProductosController(TiendaDb db) : Controller
{
    public async Task<IActionResult> Index() => View(await db.Productos.ToListAsync());
    [HttpPost, ValidateAntiForgeryToken]
    public async Task<IActionResult> Crear(Producto p)
    {
        if (!ModelState.IsValid) return View(p);
        db.Add(p); await db.SaveChangesAsync();
        return RedirectToAction(nameof(Index));
    }
}
```
```html
@model List<Producto>
@foreach (var p in Model) { <tr><td>@p.Nombre</td><td>@p.Precio.ToString("C")</td></tr> }
<form asp-action="Crear" method="post"><input asp-for="Nombre" /><span asp-validation-for="Nombre"></span></form>
```

## 9. Pruebas con xUnit

```csharp
public class CalculadoraTests
{
    [Fact] public void Suma() => Assert.Equal(5, new Calculadora().Sumar(2, 3));
    [Theory, InlineData(2, true), InlineData(3, false)]
    public void EsPar(int n, bool esperado) => Assert.Equal(esperado, n % 2 == 0);
    [Fact] public void DivisionPorCero() => Assert.Throws<DivideByZeroException>(() => { int c = 0; _ = 1 / c; });
}
```
`dotnet test`

## 10. Conceptos .NET para entrevista

- **.NET vs .NET Framework:** .NET (5, 6, 7, 8, 9...) es multiplataforma y moderno; .NET Framework (4.x) es solo Windows y heredado.
- **CLR:** máquina virtual que ejecuta el código intermedio (IL) compilado de C#.
- **NuGet:** gestor de paquetes (como npm o pip).
- **Inyección de dependencias:** se registra en `builder.Services` y el framework la entrega por constructor.
- **Middleware:** tubería de componentes por la que pasa cada petición (auth, CORS, errores).
- **`async/await` + `Task`:** asincronía sin bloquear hilos.
- **Value types vs reference types:** `struct`/`int` se copian; `class` se pasa por referencia.
- **Garbage Collector:** libera memoria automáticamente.
