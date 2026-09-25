# Cheatsheet Java ampliado (consola, POO, colecciones, JDBC, Maven, Spring Boot)

> Ejemplo ejecutable: `05-ejemplos/java/Basicos.java` → `java Basicos.java`. Proyecto: `02-proyectos/java-consola-poo/` y su versión con retos en `06-retos-resueltos/java-consola-poo/`.

## 1. Entornos y ejecución

| Herramienta | Cómo ejecutar |
|---|---|
| Terminal | `javac -encoding UTF-8 Main.java` → `java Main` (o `java Main.java` en Java 11+) |
| VS Code + Extension Pack for Java | Botón **Run** sobre `main` |
| NetBeans | Nuevo proyecto → Java with Ant/Maven → Java Application → `F6` |
| IntelliJ IDEA | New Project → Java → botón ▶ verde |
| Eclipse | File → New → Java Project → clic derecho → Run As → Java Application |

Estructura de un proyecto con paquetes:
```
src/
└── ec/edu/iste/biblioteca/
    ├── Main.java            (package ec.edu.iste.biblioteca;)
    ├── modelo/Libro.java    (package ec.edu.iste.biblioteca.modelo;)
    └── servicio/Catalogo.java
```
```bash
javac -d out -encoding UTF-8 $(find src -name "*.java")      # Linux/Git Bash
java -cp out ec.edu.iste.biblioteca.Main
```

## 2. Recordatorios de sintaxis

```java
// Tipos primitivos: byte short int long float double char boolean
// Envolturas: Integer Double Boolean... (para colecciones)
int x = Integer.parseInt("5"); double d = Double.parseDouble("3.5"); String s = String.valueOf(10);
String t = "a".repeat(3); boolean igual = s1.equals(s2);        // nunca == para Strings
final int MAX = 10;                                            // constante
var lista = new ArrayList<String>();                           // inferencia local
String texto = switch (op) { case 1 -> "Uno"; default -> "Otro"; };
if (obj instanceof Libro l) { l.getTitulo(); }                 // pattern matching
record Punto(int x, int y) {}                                  // clase de datos inmutable
```

## 3. POO: los 4 pilares con Java

```java
public abstract class Cuenta {                    // ABSTRACCIÓN
    private double saldo;                         // ENCAPSULAMIENTO: private + getters
    protected final String numero;
    public Cuenta(String numero) { this.numero = numero; }
    public double getSaldo() { return saldo; }
    public void depositar(double m) {
        if (m <= 0) throw new IllegalArgumentException("Monto inválido");
        saldo += m;
    }
    protected void setSaldo(double s) { saldo = s; }
    public abstract double interesMensual();      // cada subclase lo define
}

public class CuentaAhorros extends Cuenta {       // HERENCIA
    public CuentaAhorros(String n) { super(n); }
    @Override
    public double interesMensual() { return getSaldo() * 0.004; }   // POLIMORFISMO
}

public interface Notificable { void notificar(String msg); }        // interfaz: contrato
public class CuentaCorriente extends Cuenta implements Notificable { ... }

List<Cuenta> cuentas = List.of(new CuentaAhorros("A1"), new CuentaCorriente("C1"));
for (Cuenta c : cuentas) System.out.println(c.interesMensual());   // cada una responde distinto
```
Sobrecarga (mismo nombre, distintos parámetros, en la misma clase) ≠ sobrescritura (`@Override`, misma firma, en la subclase).

**`equals` y `hashCode`:** si dos objetos son "iguales" para ti (misma cédula), sobrescribe ambos para que funcionen en `HashSet`/`HashMap`:
```java
@Override public boolean equals(Object o) { return o instanceof Estudiante e && cedula.equals(e.cedula); }
@Override public int hashCode() { return Objects.hash(cedula); }
```

## 4. Colecciones: cuál usar

| Necesito | Clase | Complejidad típica |
|---|---|---|
| Lista ordenada por posición | `ArrayList` | get O(1), add O(1), remove O(n) |
| Muchas inserciones/borrados al inicio | `LinkedList` / `ArrayDeque` | O(1) en extremos |
| Clave → valor | `HashMap` | O(1) |
| Clave → valor manteniendo orden de inserción | `LinkedHashMap` | O(1) |
| Clave → valor ordenado por clave | `TreeMap` | O(log n) |
| Sin duplicados | `HashSet` / `TreeSet` (ordenado) | O(1) / O(log n) |
| Pila | `ArrayDeque` (`push`/`pop`) | O(1) |
| Cola | `ArrayDeque` / `LinkedList` (`offer`/`poll`) | O(1) |
| Cola de prioridad | `PriorityQueue` | O(log n) |

```java
Map<String, List<String>> porCarrera = new HashMap<>();
porCarrera.computeIfAbsent("Software", k -> new ArrayList<>()).add("Ana");
lista.sort(Comparator.comparing(Estudiante::getPromedio).reversed().thenComparing(Estudiante::getNombre));
Collections.unmodifiableList(lista); List.copyOf(lista);
Iterator<String> it = lista.iterator(); while (it.hasNext()) if (it.next().isBlank()) it.remove();
```

## 5. Streams (lo que más se pregunta en Java moderno)

```java
List<Estudiante> aprobados = estudiantes.stream().filter(e -> e.getNota() >= 7).toList();
double promedio = estudiantes.stream().mapToDouble(Estudiante::getNota).average().orElse(0);
Map<String, List<Estudiante>> porCarrera = estudiantes.stream().collect(Collectors.groupingBy(Estudiante::getCarrera));
Map<String, Double> promPorCarrera = estudiantes.stream()
    .collect(Collectors.groupingBy(Estudiante::getCarrera, Collectors.averagingDouble(Estudiante::getNota)));
Map<String, Long> conteo = palabras.stream().collect(Collectors.groupingBy(w -> w, TreeMap::new, Collectors.counting()));
Optional<Estudiante> mejor = estudiantes.stream().max(Comparator.comparingDouble(Estudiante::getNota));
String csv = nombres.stream().collect(Collectors.joining(","));
List<Integer> cuadrados = IntStream.rangeClosed(1, 10).map(i -> i * i).boxed().toList();
boolean hayReprobados = estudiantes.stream().anyMatch(e -> e.getNota() < 7);
List<String> unicos = lista.stream().distinct().sorted().limit(5).toList();
```

## 6. Archivos

```java
import java.nio.file.*;
Path ruta = Path.of("datos.csv");
Files.writeString(ruta, "codigo,nombre\nP01,Mouse\n");
Files.writeString(ruta, "P02,Teclado\n", StandardOpenOption.APPEND);
List<String> lineas = Files.readAllLines(ruta);
lineas.stream().skip(1).map(l -> l.split(",")).forEach(p -> System.out.println(p[1]));
Files.exists(ruta); Files.deleteIfExists(ruta);
try (BufferedReader br = Files.newBufferedReader(ruta)) { String l; while ((l = br.readLine()) != null) { } }
// try-with-resources cierra el archivo automáticamente
```

## 7. JDBC: CRUD con MySQL o SQLite

Driver (jar) en el classpath: `mysql-connector-j-9.x.jar` o `sqlite-jdbc-3.x.jar`, o como dependencia de Maven.
```java
import java.sql.*;

public class ProductoDAO {                          // DAO = Data Access Object
    private static final String URL = "jdbc:mysql://localhost:3306/tienda";   // SQLite: "jdbc:sqlite:tienda.db"
    private Connection conectar() throws SQLException { return DriverManager.getConnection(URL, "root", ""); }

    public int crear(String nombre, double precio) throws SQLException {
        String sql = "INSERT INTO productos (nombre, precio) VALUES (?, ?)";
        try (Connection c = conectar(); PreparedStatement ps = c.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, nombre);
            ps.setDouble(2, precio);
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) { return rs.next() ? rs.getInt(1) : -1; }
        }
    }

    public List<Producto> listar() throws SQLException {
        List<Producto> lista = new ArrayList<>();
        try (Connection c = conectar(); PreparedStatement ps = c.prepareStatement("SELECT * FROM productos ORDER BY nombre");
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) lista.add(new Producto(rs.getInt("id"), rs.getString("nombre"), rs.getDouble("precio")));
        }
        return lista;
    }

    public boolean actualizarPrecio(int id, double precio) throws SQLException {
        try (Connection c = conectar(); PreparedStatement ps = c.prepareStatement("UPDATE productos SET precio = ? WHERE id = ?")) {
            ps.setDouble(1, precio); ps.setInt(2, id);
            return ps.executeUpdate() > 0;
        }
    }

    public boolean eliminar(int id) throws SQLException {
        try (Connection c = conectar(); PreparedStatement ps = c.prepareStatement("DELETE FROM productos WHERE id = ?")) {
            ps.setInt(1, id);
            return ps.executeUpdate() > 0;
        }
    }
}
// Transacción: c.setAutoCommit(false); ... c.commit(); / c.rollback();
```
Compilar y ejecutar con el jar: `javac -cp .;mysql-connector-j.jar *.java` → `java -cp .;mysql-connector-j.jar Main` (en Linux/Mac usa `:` en lugar de `;`).

## 8. Maven (gestor de proyectos y dependencias)

```bash
mvn -v
mvn archetype:generate -DgroupId=ec.edu.iste -DartifactId=app -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false
mvn compile      mvn test      mvn package (genera target/app.jar)      mvn clean
```
```xml
<!-- pom.xml: dependencias -->
<dependency><groupId>com.mysql</groupId><artifactId>mysql-connector-j</artifactId><version>9.1.0</version></dependency>
<dependency><groupId>org.junit.jupiter</groupId><artifactId>junit-jupiter</artifactId><version>5.11.0</version><scope>test</scope></dependency>
```
Estructura Maven: `src/main/java`, `src/main/resources`, `src/test/java`.

## 9. JUnit 5

```java
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class CalculadoraTest {
    Calculadora calc;
    @BeforeEach void setUp() { calc = new Calculadora(); }
    @Test void sumaDosNumeros() { assertEquals(5, calc.sumar(2, 3)); }
    @Test void divisionPorCero() { assertThrows(ArithmeticException.class, () -> calc.dividir(1, 0)); }
    @Test @DisplayName("Promedio con decimales") void promedio() { assertEquals(8.5, calc.promedio(8, 9), 0.001); }
}
```

## 10. Spring Boot en 5 minutos (API REST)

Crear en https://start.spring.io: Maven, Java 21, dependencias **Spring Web**, **Spring Data JPA**, **H2** (o MySQL Driver), **Validation**.
```bash
./mvnw spring-boot:run          # Windows: mvnw.cmd spring-boot:run  → http://localhost:8080
```
```java
@Entity
public class Producto {
    @Id @GeneratedValue(strategy = GenerationType.IDENTITY) private Long id;
    @NotBlank private String nombre;
    @Positive private double precio;
    // getters y setters
}

public interface ProductoRepository extends JpaRepository<Producto, Long> {
    List<Producto> findByNombreContainingIgnoreCase(String texto);     // consulta derivada del nombre del método
}

@RestController
@RequestMapping("/api/productos")
public class ProductoController {
    private final ProductoRepository repo;
    public ProductoController(ProductoRepository repo) { this.repo = repo; }   // inyección de dependencias

    @GetMapping public List<Producto> listar() { return repo.findAll(); }
    @GetMapping("/{id}") public ResponseEntity<Producto> obtener(@PathVariable Long id) {
        return repo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }
    @PostMapping public ResponseEntity<Producto> crear(@Valid @RequestBody Producto p) {
        return ResponseEntity.status(HttpStatus.CREATED).body(repo.save(p));
    }
    @PutMapping("/{id}") public ResponseEntity<Producto> actualizar(@PathVariable Long id, @Valid @RequestBody Producto p) {
        if (!repo.existsById(id)) return ResponseEntity.notFound().build();
        p.setId(id); return ResponseEntity.ok(repo.save(p));
    }
    @DeleteMapping("/{id}") public ResponseEntity<Void> eliminar(@PathVariable Long id) {
        if (!repo.existsById(id)) return ResponseEntity.notFound().build();
        repo.deleteById(id); return ResponseEntity.noContent().build();
    }
}
```
`application.properties` con MySQL:
```
spring.datasource.url=jdbc:mysql://localhost:3306/tienda
spring.datasource.username=root
spring.datasource.password=
spring.jpa.hibernate.ddl-auto=update
```
Capas: **Controller** (HTTP) → **Service** (lógica) → **Repository** (datos) → **Entity** (tabla).

## 11. Errores frecuentes en Java

| Error | Causa |
|---|---|
| `error: class X is public, should be declared in a file named X.java` | El nombre del archivo no coincide con la clase |
| `error: cannot find symbol` | Variable o método mal escrito, o falta el import |
| `Exception in thread "main" java.lang.NullPointerException` | Usaste un objeto null |
| `InputMismatchException` (Scanner) | Esperaba un número y se escribió texto |
| El Scanner "se salta" un `nextLine()` | Después de `nextInt()` queda el Enter: agrega un `sc.nextLine()` extra |
| `ConcurrentModificationException` | Modificaste una lista mientras la recorrías con for-each: usa `removeIf` o un `Iterator` |
| `ClassNotFoundException: com.mysql...` | Falta el jar del driver en el classpath |
| `unmappable character for encoding` | Compila con `-encoding UTF-8` |
