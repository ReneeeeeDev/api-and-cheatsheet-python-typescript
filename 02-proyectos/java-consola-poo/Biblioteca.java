import java.util.*;
import java.util.stream.*;

/**
 * Sistema de biblioteca en consola: CRUD + POO (herencia, interfaz, polimorfismo,
 * encapsulamiento, excepciones propias) + colecciones y streams.
 *
 * Compilar y ejecutar (Java 17+):
 *   javac Biblioteca.java
 *   java Biblioteca
 * Ejecutar las pruebas:
 *   java Biblioteca --test
 */
public class Biblioteca {

    // ======================================================== MODELO (POO)
    /** Abstracción: no se puede instanciar Material directamente. */
    static abstract class Material implements Comparable<Material> {
        private static int contador = 1;          // static: compartido por todas las instancias
        private final int id;                      // encapsulamiento: private + getters
        private String titulo;
        private int anio;
        private boolean prestado;

        Material(String titulo, int anio) {
            this.id = contador++;
            setTitulo(titulo);
            setAnio(anio);
        }

        public int getId() { return id; }
        public String getTitulo() { return titulo; }
        public int getAnio() { return anio; }
        public boolean isPrestado() { return prestado; }

        public void setTitulo(String titulo) {
            if (titulo == null || titulo.isBlank()) throw new IllegalArgumentException("Título obligatorio");
            this.titulo = titulo.trim();
        }
        public void setAnio(int anio) {
            if (anio < 1450 || anio > 2100) throw new IllegalArgumentException("Año inválido");
            this.anio = anio;
        }
        void setPrestado(boolean p) { this.prestado = p; }

        /** Polimorfismo: cada subclase define sus días de préstamo. */
        public abstract int diasPrestamo();
        public abstract String tipo();

        @Override public int compareTo(Material o) { return titulo.compareToIgnoreCase(o.titulo); }

        @Override public String toString() {
            return String.format("#%-3d %-8s %-35s %d  %s", id, tipo(), titulo, anio,
                    prestado ? "[PRESTADO]" : "[disponible]");
        }
    }

    static class Libro extends Material {           // herencia
        private final String autor;
        Libro(String titulo, int anio, String autor) { super(titulo, anio); this.autor = autor; }
        public String getAutor() { return autor; }
        @Override public int diasPrestamo() { return 15; }
        @Override public String tipo() { return "Libro"; }
        @Override public String toString() { return super.toString() + "  (" + autor + ")"; }
    }

    static class Revista extends Material {
        private final int edicion;
        Revista(String titulo, int anio, int edicion) { super(titulo, anio); this.edicion = edicion; }
        @Override public int diasPrestamo() { return 5; }
        @Override public String tipo() { return "Revista"; }
        @Override public String toString() { return super.toString() + "  (ed. " + edicion + ")"; }
    }

    /** Excepción propia (checked). */
    static class BibliotecaException extends Exception {
        BibliotecaException(String msg) { super(msg); }
    }

    // ======================================================== SERVICIO (lógica / "repositorio")
    static class Catalogo {
        private final Map<Integer, Material> materiales = new LinkedHashMap<>();

        public Material agregar(Material m) { materiales.put(m.getId(), m); return m; }

        public List<Material> listar() { return new ArrayList<>(materiales.values()); }

        public Material buscarPorId(int id) throws BibliotecaException {
            Material m = materiales.get(id);
            if (m == null) throw new BibliotecaException("No existe el material #" + id);
            return m;
        }

        public List<Material> buscarPorTitulo(String texto) {
            String t = texto.toLowerCase();
            return materiales.values().stream()
                    .filter(m -> m.getTitulo().toLowerCase().contains(t))
                    .sorted()
                    .collect(Collectors.toList());
        }

        public void actualizar(int id, String titulo, int anio) throws BibliotecaException {
            Material m = buscarPorId(id);
            m.setTitulo(titulo);
            m.setAnio(anio);
        }

        public void eliminar(int id) throws BibliotecaException {
            Material m = buscarPorId(id);
            if (m.isPrestado()) throw new BibliotecaException("No se puede eliminar: está prestado");
            materiales.remove(id);
        }

        public int prestar(int id) throws BibliotecaException {
            Material m = buscarPorId(id);
            if (m.isPrestado()) throw new BibliotecaException("Ya está prestado");
            m.setPrestado(true);
            return m.diasPrestamo();
        }

        public void devolver(int id) throws BibliotecaException {
            Material m = buscarPorId(id);
            if (!m.isPrestado()) throw new BibliotecaException("No estaba prestado");
            m.setPrestado(false);
        }

        /** Streams: agrupar y contar por tipo. */
        public Map<String, Long> conteoPorTipo() {
            return materiales.values().stream()
                    .collect(Collectors.groupingBy(Material::tipo, TreeMap::new, Collectors.counting()));
        }

        public Optional<Material> masAntiguo() {
            return materiales.values().stream().min(Comparator.comparingInt(Material::getAnio));
        }

        public double promedioAnio() {
            return materiales.values().stream().mapToInt(Material::getAnio).average().orElse(0);
        }
    }

    // ======================================================== INTERFAZ DE CONSOLA
    private static final Scanner sc = new Scanner(System.in);

    static int leerEntero(String msg) {
        while (true) {
            System.out.print(msg);
            try {
                return Integer.parseInt(sc.nextLine().trim());
            } catch (NumberFormatException e) {
                System.out.println("  -> Ingrese un número válido.");
            }
        }
    }

    static String leerTexto(String msg) {
        System.out.print(msg);
        return sc.nextLine();
    }

    static Catalogo datosIniciales() {
        Catalogo c = new Catalogo();
        c.agregar(new Libro("Cien años de soledad", 1967, "Gabriel García Márquez"));
        c.agregar(new Libro("Huasipungo", 1934, "Jorge Icaza"));
        c.agregar(new Libro("Clean Code", 2008, "Robert C. Martin"));
        c.agregar(new Revista("National Geographic", 2024, 312));
        return c;
    }

    public static void main(String[] args) {
        if (args.length > 0 && args[0].equals("--test")) { Pruebas.ejecutar(); return; }

        Catalogo catalogo = datosIniciales();
        int opcion;
        do {
            System.out.println("\n===== BIBLIOTECA =====");
            System.out.println("1. Listar   2. Buscar   3. Agregar libro   4. Agregar revista");
            System.out.println("5. Editar   6. Eliminar 7. Prestar         8. Devolver");
            System.out.println("9. Estadísticas         0. Salir");
            opcion = leerEntero("Opción: ");
            try {
                switch (opcion) {
                    case 1 -> catalogo.listar().forEach(System.out::println);
                    case 2 -> {
                        List<Material> r = catalogo.buscarPorTitulo(leerTexto("Texto a buscar: "));
                        if (r.isEmpty()) System.out.println("Sin resultados.");
                        r.forEach(System.out::println);
                    }
                    case 3 -> System.out.println("Creado: " + catalogo.agregar(new Libro(
                            leerTexto("Título: "), leerEntero("Año: "), leerTexto("Autor: "))));
                    case 4 -> System.out.println("Creado: " + catalogo.agregar(new Revista(
                            leerTexto("Título: "), leerEntero("Año: "), leerEntero("Edición: "))));
                    case 5 -> {
                        int id = leerEntero("ID: ");
                        catalogo.buscarPorId(id);                 // valida antes de pedir datos
                        catalogo.actualizar(id, leerTexto("Nuevo título: "), leerEntero("Nuevo año: "));
                        System.out.println("Actualizado.");
                    }
                    case 6 -> { catalogo.eliminar(leerEntero("ID: ")); System.out.println("Eliminado."); }
                    case 7 -> System.out.println("Prestado por " + catalogo.prestar(leerEntero("ID: ")) + " días.");
                    case 8 -> { catalogo.devolver(leerEntero("ID: ")); System.out.println("Devuelto."); }
                    case 9 -> {
                        System.out.println("Por tipo: " + catalogo.conteoPorTipo());
                        System.out.printf("Año promedio: %.1f%n", catalogo.promedioAnio());
                        catalogo.masAntiguo().ifPresent(m -> System.out.println("Más antiguo: " + m.getTitulo()));
                    }
                    case 0 -> System.out.println("¡Hasta luego!");
                    default -> System.out.println("Opción inválida.");
                }
            } catch (BibliotecaException | IllegalArgumentException e) {
                System.out.println("  ERROR: " + e.getMessage());
            }
        } while (opcion != 0);
    }

    // ======================================================== PRUEBAS (sin JUnit)
    static class Pruebas {
        static int ok = 0, fallos = 0;

        static void check(String nombre, boolean condicion) {
            if (condicion) { ok++; System.out.println("  OK    " + nombre); }
            else { fallos++; System.out.println("  FALLO " + nombre); }
        }

        static void ejecutar() {
            Catalogo c = datosIniciales();
            check("lista 4 materiales", c.listar().size() == 4);
            check("búsqueda ignora mayúsculas", c.buscarPorTitulo("CLEAN").size() == 1);
            check("polimorfismo días libro=15", new Libro("X", 2000, "Y").diasPrestamo() == 15);
            check("polimorfismo días revista=5", new Revista("X", 2000, 1).diasPrestamo() == 5);
            check("conteo por tipo", c.conteoPorTipo().get("Libro") == 3L);
            check("más antiguo es Huasipungo", c.masAntiguo().get().getTitulo().equals("Huasipungo"));
            try {
                int id = c.listar().get(0).getId();
                c.prestar(id);
                boolean lanzo = false;
                try { c.eliminar(id); } catch (BibliotecaException e) { lanzo = true; }
                check("no elimina prestado", lanzo);
                c.devolver(id);
                c.eliminar(id);
                check("elimina tras devolver", c.listar().size() == 3);
            } catch (BibliotecaException e) { check("flujo préstamo: " + e.getMessage(), false); }
            boolean lanzo = false;
            try { new Libro("", 2000, "A"); } catch (IllegalArgumentException e) { lanzo = true; }
            check("valida título vacío", lanzo);
            System.out.printf("%nResultado: %d OK, %d fallos%n", ok, fallos);
            if (fallos > 0) System.exit(1);
        }
    }
}
