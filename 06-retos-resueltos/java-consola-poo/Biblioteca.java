import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.*;

/**
 * Biblioteca con los 3 RETOS resueltos:
 *   RETO 1: clase Tesis (3 días de préstamo)
 *   RETO 2: guardar y cargar el catálogo en CSV (java.nio.file.Files)
 *   RETO 3: clase Usuario + registro de quién tiene cada préstamo (límite, fecha límite y multa)
 *
 * Compilar y ejecutar (Java 17+):
 *   javac -encoding UTF-8 Biblioteca.java
 *   java Biblioteca            (menú)
 *   java Biblioteca --test     (pruebas)
 */
public class Biblioteca {

    // ======================================================== MODELO
    static abstract class Material implements Comparable<Material> {
        private static int contador = 1;
        private final int id;
        private String titulo;
        private int anio;

        Material(String titulo, int anio) { this(contador, titulo, anio); }

        /** Constructor usado al cargar desde CSV (conserva el id original). */
        Material(int id, String titulo, int anio) {
            this.id = id;
            contador = Math.max(contador, id + 1);
            setTitulo(titulo);
            setAnio(anio);
        }

        public int getId() { return id; }
        public String getTitulo() { return titulo; }
        public int getAnio() { return anio; }
        public void setTitulo(String t) {
            if (t == null || t.isBlank()) throw new IllegalArgumentException("Título obligatorio");
            this.titulo = t.trim();
        }
        public void setAnio(int a) {
            if (a < 1450 || a > 2100) throw new IllegalArgumentException("Año inválido");
            this.anio = a;
        }

        public abstract int diasPrestamo();
        public abstract String tipo();
        /** Campos propios de cada subclase para el CSV. */
        protected abstract String extraCsv();

        public String aCsv() { return String.join(";", tipo(), String.valueOf(id), limpiar(titulo), String.valueOf(anio), extraCsv()); }
        static String limpiar(String s) { return s.replace(";", ","); }   // ; es el separador

        @Override public int compareTo(Material o) { return titulo.compareToIgnoreCase(o.titulo); }
        @Override public String toString() { return String.format("#%-3d %-8s %-35s %d", id, tipo(), titulo, anio); }
    }

    static class Libro extends Material {
        private final String autor;
        Libro(String t, int a, String autor) { super(t, a); this.autor = autor; }
        Libro(int id, String t, int a, String autor) { super(id, t, a); this.autor = autor; }
        @Override public int diasPrestamo() { return 15; }
        @Override public String tipo() { return "Libro"; }
        @Override protected String extraCsv() { return limpiar(autor); }
        @Override public String toString() { return super.toString() + "  (" + autor + ")"; }
    }

    static class Revista extends Material {
        private final int edicion;
        Revista(String t, int a, int e) { super(t, a); edicion = e; }
        Revista(int id, String t, int a, int e) { super(id, t, a); edicion = e; }
        @Override public int diasPrestamo() { return 5; }
        @Override public String tipo() { return "Revista"; }
        @Override protected String extraCsv() { return String.valueOf(edicion); }
        @Override public String toString() { return super.toString() + "  (ed. " + edicion + ")"; }
    }

    /** RETO 1: nueva subclase. Gracias al polimorfismo, el resto del código no cambia. */
    static class Tesis extends Material {
        private final String autor;
        private final String carrera;
        Tesis(String t, int a, String autor, String carrera) { super(t, a); this.autor = autor; this.carrera = carrera; }
        Tesis(int id, String t, int a, String autor, String carrera) { super(id, t, a); this.autor = autor; this.carrera = carrera; }
        @Override public int diasPrestamo() { return 3; }
        @Override public String tipo() { return "Tesis"; }
        @Override protected String extraCsv() { return limpiar(autor) + ";" + limpiar(carrera); }
        @Override public String toString() { return super.toString() + "  (" + autor + " - " + carrera + ")"; }
    }

    /** RETO 3: usuario de la biblioteca. */
    static class Usuario {
        static final int MAX_PRESTAMOS = 3;
        private final String cedula;
        private final String nombre;
        Usuario(String cedula, String nombre) {
            if (cedula == null || !cedula.matches("\\d{10}")) throw new IllegalArgumentException("Cédula debe tener 10 dígitos");
            if (nombre == null || nombre.isBlank()) throw new IllegalArgumentException("Nombre obligatorio");
            this.cedula = cedula; this.nombre = nombre.trim();
        }
        public String getCedula() { return cedula; }
        public String getNombre() { return nombre; }
        @Override public String toString() { return cedula + " " + nombre; }
    }

    /** RETO 3: préstamo = quién, qué y hasta cuándo. record: inmutable. */
    record Prestamo(Material material, Usuario usuario, LocalDate desde, LocalDate hasta) {
        long diasAtraso(LocalDate hoy) { return Math.max(0, ChronoUnit.DAYS.between(hasta, hoy)); }
        double multa(LocalDate hoy) { return diasAtraso(hoy) * Catalogo.MULTA_POR_DIA; }
    }

    static class BibliotecaException extends Exception {
        BibliotecaException(String msg) { super(msg); }
    }

    // ======================================================== SERVICIO
    static class Catalogo {
        static final double MULTA_POR_DIA = 0.25;
        private final Map<Integer, Material> materiales = new LinkedHashMap<>();
        private final Map<String, Usuario> usuarios = new LinkedHashMap<>();
        private final Map<Integer, Prestamo> prestamos = new LinkedHashMap<>();   // idMaterial -> préstamo activo

        public Material agregar(Material m) { materiales.put(m.getId(), m); return m; }
        public List<Material> listar() { return new ArrayList<>(materiales.values()); }

        public Material buscarPorId(int id) throws BibliotecaException {
            Material m = materiales.get(id);
            if (m == null) throw new BibliotecaException("No existe el material #" + id);
            return m;
        }

        public List<Material> buscarPorTitulo(String texto) {
            String t = texto.toLowerCase();
            return materiales.values().stream().filter(m -> m.getTitulo().toLowerCase().contains(t)).sorted().toList();
        }

        public void actualizar(int id, String titulo, int anio) throws BibliotecaException {
            Material m = buscarPorId(id);
            m.setTitulo(titulo);
            m.setAnio(anio);
        }

        public void eliminar(int id) throws BibliotecaException {
            buscarPorId(id);
            if (prestamos.containsKey(id)) throw new BibliotecaException("No se puede eliminar: está prestado");
            materiales.remove(id);
        }

        // ---------- RETO 3: usuarios y préstamos
        public Usuario registrarUsuario(String cedula, String nombre) throws BibliotecaException {
            if (usuarios.containsKey(cedula)) throw new BibliotecaException("Ya existe un usuario con cédula " + cedula);
            Usuario u = new Usuario(cedula, nombre);
            usuarios.put(cedula, u);
            return u;
        }

        public Usuario buscarUsuario(String cedula) throws BibliotecaException {
            Usuario u = usuarios.get(cedula);
            if (u == null) throw new BibliotecaException("No existe el usuario " + cedula);
            return u;
        }

        public List<Usuario> listarUsuarios() { return new ArrayList<>(usuarios.values()); }

        public List<Prestamo> prestamosDe(String cedula) {
            return prestamos.values().stream().filter(p -> p.usuario().getCedula().equals(cedula)).toList();
        }

        public Prestamo prestar(int idMaterial, String cedula, LocalDate hoy) throws BibliotecaException {
            Material m = buscarPorId(idMaterial);
            Usuario u = buscarUsuario(cedula);
            if (prestamos.containsKey(idMaterial)) {
                throw new BibliotecaException("Ya está prestado a " + prestamos.get(idMaterial).usuario().getNombre());
            }
            if (prestamosDe(cedula).size() >= Usuario.MAX_PRESTAMOS) {
                throw new BibliotecaException(u.getNombre() + " ya tiene " + Usuario.MAX_PRESTAMOS + " préstamos (máximo)");
            }
            boolean tieneAtrasos = prestamosDe(cedula).stream().anyMatch(p -> p.diasAtraso(hoy) > 0);
            if (tieneAtrasos) throw new BibliotecaException(u.getNombre() + " tiene préstamos atrasados");
            Prestamo p = new Prestamo(m, u, hoy, hoy.plusDays(m.diasPrestamo()));   // polimorfismo decide los días
            prestamos.put(idMaterial, p);
            return p;
        }

        /** Devuelve la multa a pagar (0 si está a tiempo). */
        public double devolver(int idMaterial, LocalDate hoy) throws BibliotecaException {
            buscarPorId(idMaterial);
            Prestamo p = prestamos.remove(idMaterial);
            if (p == null) throw new BibliotecaException("No estaba prestado");
            return p.multa(hoy);
        }

        public boolean estaPrestado(int idMaterial) { return prestamos.containsKey(idMaterial); }
        public List<Prestamo> prestamosActivos() { return new ArrayList<>(prestamos.values()); }

        public List<Prestamo> atrasados(LocalDate hoy) {
            return prestamos.values().stream().filter(p -> p.diasAtraso(hoy) > 0)
                    .sorted(Comparator.comparing(Prestamo::hasta)).toList();
        }

        public Map<String, Long> conteoPorTipo() {
            return materiales.values().stream().collect(Collectors.groupingBy(Material::tipo, TreeMap::new, Collectors.counting()));
        }

        // ---------- RETO 2: persistencia CSV
        public void guardarCsv(Path ruta) throws IOException {
            List<String> lineas = new ArrayList<>();
            lineas.add("tipo;id;titulo;anio;extra1;extra2");
            for (Material m : materiales.values()) lineas.add(m.aCsv());
            Files.write(ruta, lineas, StandardCharsets.UTF_8);
        }

        /** Carga y REEMPLAZA el catálogo. Devuelve cuántas líneas se omitieron por error. */
        public int cargarCsv(Path ruta) throws IOException {
            List<String> lineas = Files.readAllLines(ruta, StandardCharsets.UTF_8);
            materiales.clear();
            prestamos.clear();
            int errores = 0;
            for (String linea : lineas.subList(Math.min(1, lineas.size()), lineas.size())) {   // salta encabezado
                if (linea.isBlank()) continue;
                String[] c = linea.split(";", -1);
                try {
                    int id = Integer.parseInt(c[1]);
                    int anio = Integer.parseInt(c[3]);
                    Material m = switch (c[0]) {
                        case "Libro" -> new Libro(id, c[2], anio, c[4]);
                        case "Revista" -> new Revista(id, c[2], anio, Integer.parseInt(c[4]));
                        case "Tesis" -> new Tesis(id, c[2], anio, c[4], c[5]);
                        default -> throw new IllegalArgumentException("Tipo desconocido: " + c[0]);
                    };
                    agregar(m);
                } catch (RuntimeException e) {     // NumberFormat, índice fuera de rango, tipo inválido
                    errores++;
                    System.out.println("  Línea omitida (" + e.getMessage() + "): " + linea);
                }
            }
            return errores;
        }
    }

    // ======================================================== CONSOLA
    private static final Scanner sc = new Scanner(System.in);
    private static final Path ARCHIVO = Path.of("catalogo.csv");

    static int leerEntero(String msg) {
        while (true) {
            System.out.print(msg);
            try { return Integer.parseInt(sc.nextLine().trim()); }
            catch (NumberFormatException e) { System.out.println("  -> Ingrese un número válido."); }
        }
    }

    static String leerTexto(String msg) { System.out.print(msg); return sc.nextLine(); }

    static Catalogo datosIniciales() {
        Catalogo c = new Catalogo();
        c.agregar(new Libro("Cien años de soledad", 1967, "Gabriel García Márquez"));
        c.agregar(new Libro("Huasipungo", 1934, "Jorge Icaza"));
        c.agregar(new Libro("Clean Code", 2008, "Robert C. Martin"));
        c.agregar(new Revista("National Geographic", 2024, 312));
        c.agregar(new Tesis("Sistema de reservas de laboratorios", 2025, "Ana Pérez", "Desarrollo de Software"));
        try {
            c.registrarUsuario("1710034065", "Ana Pérez");
            c.registrarUsuario("0926687856", "Luis Mora");
        } catch (BibliotecaException e) { throw new IllegalStateException(e); }
        return c;
    }

    public static void main(String[] args) {
        if (args.length > 0 && args[0].equals("--test")) { Pruebas.ejecutar(); return; }

        Catalogo catalogo = datosIniciales();
        if (Files.exists(ARCHIVO)) {
            try { catalogo.cargarCsv(ARCHIVO); System.out.println("Catálogo cargado de " + ARCHIVO.toAbsolutePath()); }
            catch (IOException e) { System.out.println("No se pudo leer el CSV: " + e.getMessage()); }
        }
        int op;
        do {
            System.out.println("\n===== BIBLIOTECA =====");
            System.out.println(" 1. Listar materiales      2. Buscar            3. Agregar libro     4. Agregar revista");
            System.out.println(" 5. Agregar tesis          6. Editar            7. Eliminar");
            System.out.println(" 8. Registrar usuario      9. Listar usuarios  10. Prestar         11. Devolver");
            System.out.println("12. Préstamos activos     13. Guardar CSV      14. Cargar CSV       0. Salir");
            op = leerEntero("Opción: ");
            try {
                LocalDate hoy = LocalDate.now();
                switch (op) {
                    case 1 -> catalogo.listar().forEach(m -> System.out.println(m + (catalogo.estaPrestado(m.getId()) ? "  [PRESTADO]" : "")));
                    case 2 -> catalogo.buscarPorTitulo(leerTexto("Texto: ")).forEach(System.out::println);
                    case 3 -> System.out.println("Creado: " + catalogo.agregar(new Libro(leerTexto("Título: "), leerEntero("Año: "), leerTexto("Autor: "))));
                    case 4 -> System.out.println("Creado: " + catalogo.agregar(new Revista(leerTexto("Título: "), leerEntero("Año: "), leerEntero("Edición: "))));
                    case 5 -> System.out.println("Creado: " + catalogo.agregar(new Tesis(leerTexto("Título: "), leerEntero("Año: "),
                            leerTexto("Autor: "), leerTexto("Carrera: "))));
                    case 6 -> {
                        int id = leerEntero("ID: ");
                        catalogo.buscarPorId(id);
                        catalogo.actualizar(id, leerTexto("Nuevo título: "), leerEntero("Nuevo año: "));
                        System.out.println("Actualizado.");
                    }
                    case 7 -> { catalogo.eliminar(leerEntero("ID: ")); System.out.println("Eliminado."); }
                    case 8 -> System.out.println("Registrado: " + catalogo.registrarUsuario(leerTexto("Cédula: "), leerTexto("Nombre: ")));
                    case 9 -> catalogo.listarUsuarios().forEach(u ->
                            System.out.println(u + " - préstamos: " + catalogo.prestamosDe(u.getCedula()).size()));
                    case 10 -> {
                        Prestamo p = catalogo.prestar(leerEntero("ID material: "), leerTexto("Cédula usuario: "), hoy);
                        System.out.println("Prestado a " + p.usuario().getNombre() + " hasta " + p.hasta());
                    }
                    case 11 -> {
                        double multa = catalogo.devolver(leerEntero("ID material: "), hoy);
                        System.out.println(multa > 0 ? String.format("Devuelto con atraso. Multa: $%.2f", multa) : "Devuelto a tiempo.");
                    }
                    case 12 -> catalogo.prestamosActivos().forEach(p -> System.out.printf("%s -> %s (hasta %s)%s%n",
                            p.material().getTitulo(), p.usuario().getNombre(), p.hasta(),
                            p.diasAtraso(hoy) > 0 ? " ATRASADO " + p.diasAtraso(hoy) + " días" : ""));
                    case 13 -> { catalogo.guardarCsv(ARCHIVO); System.out.println("Guardado en " + ARCHIVO.toAbsolutePath()); }
                    case 14 -> System.out.println("Cargado. Líneas con error: " + catalogo.cargarCsv(ARCHIVO));
                    case 0 -> System.out.println("¡Hasta luego!");
                    default -> System.out.println("Opción inválida.");
                }
            } catch (BibliotecaException | IllegalArgumentException e) {
                System.out.println("  ERROR: " + e.getMessage());
            } catch (IOException e) {
                System.out.println("  ERROR de archivo: " + e.getMessage());
            }
        } while (op != 0);
    }

    // ======================================================== PRUEBAS
    static class Pruebas {
        static int ok = 0, fallos = 0;

        static void check(String nombre, boolean cond) {
            if (cond) { ok++; System.out.println("  OK    " + nombre); }
            else { fallos++; System.out.println("  FALLO " + nombre); }
        }

        static boolean lanza(Ejecutable e) {
            try { e.run(); return false; } catch (Exception ex) { return true; }
        }
        interface Ejecutable { void run() throws Exception; }

        static void ejecutar() {
            try {
                Catalogo c = datosIniciales();
                LocalDate hoy = LocalDate.of(2026, 9, 25);

                // RETO 1
                Tesis t = new Tesis("Prueba", 2024, "X", "Software");
                check("reto1: tesis presta 3 días", t.diasPrestamo() == 3);
                check("reto1: conteo por tipo incluye Tesis", c.conteoPorTipo().get("Tesis") == 1L);

                // RETO 3
                Prestamo p = c.prestar(5, "1710034065", hoy);
                check("reto3: fecha límite de tesis = hoy + 3", p.hasta().equals(hoy.plusDays(3)));
                check("reto3: no presta material ya prestado", lanza(() -> c.prestar(5, "0926687856", hoy)));
                check("reto3: usuario inexistente", lanza(() -> c.prestar(1, "9999999999", hoy)));
                check("reto3: cédula inválida al registrar", lanza(() -> c.registrarUsuario("123", "X")));
                check("reto3: cédula duplicada", lanza(() -> c.registrarUsuario("1710034065", "Otra")));
                c.prestar(1, "1710034065", hoy);
                c.prestar(2, "1710034065", hoy);
                check("reto3: máximo 3 préstamos", lanza(() -> c.prestar(3, "1710034065", hoy)));
                check("reto3: préstamos de Ana = 3", c.prestamosDe("1710034065").size() == 3);
                check("reto3: no elimina material prestado", lanza(() -> c.eliminar(1)));
                check("reto3: atrasados a los 5 días = tesis", c.atrasados(hoy.plusDays(5)).size() == 1);
                check("reto3: multa 2 días atraso = 0.50", c.devolver(5, hoy.plusDays(5)) == 0.50);
                check("reto3: devolver a tiempo = 0", c.devolver(1, hoy.plusDays(10)) == 0.0);
                check("reto3: devolver no prestado lanza", lanza(() -> c.devolver(1, hoy)));
                c.prestar(4, "0926687856", hoy);                        // revista: 5 días
                check("reto3: con atraso no puede pedir más", lanza(() -> c.prestar(3, "0926687856", hoy.plusDays(6))));

                // RETO 2
                Path tmp = Files.createTempFile("catalogo", ".csv");
                c.guardarCsv(tmp);
                List<String> lineas = Files.readAllLines(tmp);
                check("reto2: CSV tiene encabezado + 5 materiales", lineas.size() == 6);
                Catalogo otro = new Catalogo();
                Files.writeString(tmp, "\nRevista;90;Mala;abc;1\nDVD;91;X;2000;y\n", StandardOpenOption.APPEND);
                int errores = otro.cargarCsv(tmp);
                check("reto2: carga 5 y omite 2 líneas malas", otro.listar().size() == 5 && errores == 2);
                check("reto2: conserva ids y tipos", otro.buscarPorId(5) instanceof Tesis && otro.buscarPorId(2).getTitulo().equals("Huasipungo"));
                check("reto2: nuevos ids continúan después del mayor", new Libro("Nuevo", 2020, "Z").getId() > 5);
                Files.deleteIfExists(tmp);
            } catch (Exception e) {
                check("excepción inesperada: " + e, false);
            }
            System.out.printf("%nResultado: %d OK, %d fallos%n", ok, fallos);
            if (fallos > 0) System.exit(1);
        }
    }
}
