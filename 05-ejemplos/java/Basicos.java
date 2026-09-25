import java.time.*;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.function.*;
import java.util.stream.*;

/**
 * Repaso de Java en un solo archivo: tipos, strings, arreglos, colecciones, streams, POO,
 * interfaces, records, excepciones, fechas y genéricos.
 *
 * Ejecutar (Java 17+):   java Basicos.java
 * O en dos pasos:        javac -encoding UTF-8 Basicos.java   y luego   java Basicos
 * Si ves "?" en lugar de tildes en Windows: chcp 65001
 */
public class Basicos {

    // ------------------------------------------------------------ POO
    interface Pagable {                         // interfaz = contrato
        double calcularPago();
        default String moneda() { return "USD"; }   // método por defecto
    }

    static abstract class Empleado implements Pagable, Comparable<Empleado> {
        private static int contador = 0;
        protected final int id;
        private final String nombre;

        Empleado(String nombre) {
            if (nombre == null || nombre.isBlank()) throw new IllegalArgumentException("Nombre obligatorio");
            this.id = ++contador;
            this.nombre = nombre;
        }
        public String getNombre() { return nombre; }
        public double aporteIess() { return Math.round(calcularPago() * 0.0945 * 100) / 100.0; }

        @Override public int compareTo(Empleado o) { return Double.compare(o.calcularPago(), calcularPago()); }
        @Override public String toString() {
            return String.format("#%d %-10s %-8s $%8.2f %s", id, getClass().getSimpleName(), nombre, calcularPago(), moneda());
        }
    }

    static class TiempoCompleto extends Empleado {
        private final double sueldo;
        TiempoCompleto(String n, double s) { super(n); this.sueldo = s; }
        @Override public double calcularPago() { return sueldo; }
    }

    static class PorHoras extends Empleado {
        private final int horas; private final double tarifa;
        PorHoras(String n, int h, double t) { super(n); horas = h; tarifa = t; }
        @Override public double calcularPago() { return horas * tarifa; }
    }

    // record: clase inmutable de datos (Java 16+): constructor, getters, equals, toString automáticos
    record Producto(String codigo, String nombre, double precio, int stock) {
        Producto {                                   // constructor compacto para validar
            if (precio <= 0) throw new IllegalArgumentException("Precio inválido");
        }
        double valor() { return precio * stock; }
    }

    // Excepción propia (checked)
    static class StockInsuficienteException extends Exception {
        StockInsuficienteException(String msg) { super(msg); }
    }

    static int vender(Map<String, Integer> inventario, String codigo, int cantidad) throws StockInsuficienteException {
        int actual = inventario.getOrDefault(codigo, 0);
        if (cantidad > actual) throw new StockInsuficienteException("Stock de " + codigo + " insuficiente: " + actual);
        inventario.put(codigo, actual - cantidad);
        return actual - cantidad;
    }

    // Genéricos
    static <T extends Comparable<T>> T maximo(List<T> lista) {
        T max = lista.get(0);
        for (T x : lista) if (x.compareTo(max) > 0) max = x;
        return max;
    }

    public static void main(String[] args) {
        System.out.println("===== TIPOS Y OPERADORES");
        int entero = 7; long grande = 10_000_000_000L; double dec = 7 / 2.0; char letra = 'A'; boolean ok = true;
        System.out.println(entero / 2 + " " + entero % 2 + " " + dec + " " + grande + " " + (char) (letra + 1) + " " + ok);
        System.out.println((int) 3.99 + " " + Integer.parseInt("42") + " " + Double.parseDouble("3.5") + " " + String.valueOf(10) + "0");
        System.out.println(Math.max(3, 9) + " " + Math.pow(2, 10) + " " + Math.sqrt(16) + " " + Math.round(2.5) + " " + Math.abs(-4));
        var inferido = "var infiere el tipo (Java 10+)";
        System.out.println(inferido);

        System.out.println("\n===== STRINGS");
        String s = "  Hola Mundo Java  ";
        System.out.println(s.trim() + "|" + s.strip().toUpperCase() + "|" + s.length() + "|" + s.trim().charAt(0));
        System.out.println(s.contains("Mundo") + " " + s.trim().startsWith("Hola") + " " + s.indexOf("o") + " " + s.trim().substring(5, 10));
        System.out.println(String.join("-", "2026", "09", "25") + " " + Arrays.toString("a,b,c".split(",")) + " " + "ja".repeat(3));
        String a1 = "hola", a2 = new String("hola");
        System.out.println((a1 == a2) + " " + a1.equals(a2) + " " + "HOLA".equalsIgnoreCase(a1));   // false true true
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 5; i++) sb.append(i).append(",");
        sb.setLength(sb.length() - 1);
        System.out.println(sb + " | invertido: " + new StringBuilder("hola").reverse());
        System.out.printf("%-10s|%8.2f|%05d%n", "Ana", 9.456, 42);
        String bloque = """
                Texto multilínea (Java 15+)
                  conserva la sangría relativa""";
        System.out.println(bloque);

        System.out.println("\n===== CONTROL DE FLUJO");
        int nota = 8;
        String estado = nota >= 9 ? "Excelente" : nota >= 7 ? "Aprobado" : "Reprobado";
        String dia = switch (3) {                        // switch como expresión (Java 14+)
            case 1, 7 -> "Fin de semana";
            case 2, 3, 4, 5, 6 -> "Laborable";
            default -> "Inválido";
        };
        System.out.println(estado + " " + dia);
        for (int i = 0; i < 3; i++) System.out.print(i + " ");
        int n = 5, suma = 0;
        while (n > 0) suma += n--;
        System.out.println("| suma=" + suma);

        System.out.println("\n===== ARREGLOS");
        int[] nums = {5, 3, 8, 1};
        int[] copia = Arrays.copyOf(nums, nums.length);
        Arrays.sort(copia);
        System.out.println(Arrays.toString(nums) + " " + Arrays.toString(copia) + " " + Arrays.stream(nums).sum()
                + " busqueda=" + Arrays.binarySearch(copia, 5));
        int[][] matriz = {{1, 2, 3}, {4, 5, 6}};
        System.out.println(matriz[1][2] + " " + Arrays.deepToString(matriz));
        for (int[] fila : matriz) System.out.print(Arrays.stream(fila).sum() + " ");
        System.out.println();

        System.out.println("\n===== COLECCIONES");
        List<String> lista = new ArrayList<>(List.of("pera", "uva", "kiwi"));
        lista.add("mango"); lista.remove("uva"); lista.add(0, "fresa");
        Collections.sort(lista);
        System.out.println(lista + " size=" + lista.size() + " contiene kiwi=" + lista.contains("kiwi") + " get(1)=" + lista.get(1));
        lista.removeIf(f -> f.length() > 4);
        System.out.println("removeIf: " + lista);

        Map<String, Integer> inventario = new HashMap<>();
        inventario.put("P01", 10); inventario.put("P02", 3);
        inventario.merge("P01", 5, Integer::sum);          // suma 5 al existente
        inventario.putIfAbsent("P03", 0);
        for (Map.Entry<String, Integer> e : new TreeMap<>(inventario).entrySet()) System.out.print(e.getKey() + "=" + e.getValue() + " ");
        System.out.println();

        Set<Integer> unicos = new TreeSet<>(List.of(3, 1, 3, 2));
        Deque<String> pila = new ArrayDeque<>(); pila.push("a"); pila.push("b");
        Queue<String> cola = new LinkedList<>(); cola.offer("c1"); cola.offer("c2");
        System.out.println(unicos + " pila.pop=" + pila.pop() + " cola.poll=" + cola.poll());

        // Contar palabras
        Map<String, Integer> conteo = new TreeMap<>();
        for (String p : "el perro y el gato y el loro".split(" ")) conteo.put(p, conteo.getOrDefault(p, 0) + 1);
        System.out.println(conteo);

        System.out.println("\n===== STREAMS Y LAMBDAS");
        List<Producto> productos = List.of(
                new Producto("P01", "Mouse", 15.5, 20), new Producto("P02", "Teclado", 45, 8),
                new Producto("P03", "Monitor", 139.99, 3), new Producto("P04", "Cable", 3, 0));
        List<String> conStock = productos.stream().filter(p -> p.stock() > 0).map(Producto::nombre).collect(Collectors.toList());
        double valorTotal = productos.stream().mapToDouble(Producto::valor).sum();
        Optional<Producto> masCaro = productos.stream().max(Comparator.comparingDouble(Producto::precio));
        List<Producto> ordenados = productos.stream().sorted(Comparator.comparing(Producto::nombre)).toList();
        Map<Boolean, Long> particion = productos.stream().collect(Collectors.partitioningBy(p -> p.precio() > 20, Collectors.counting()));
        String nombres = productos.stream().map(Producto::nombre).collect(Collectors.joining(", ", "[", "]"));
        System.out.println(conStock + String.format(" valor=%.2f", valorTotal) + " masCaro=" + masCaro.map(Producto::nombre).orElse("-"));
        System.out.println(ordenados.get(0) + "\n" + particion + " " + nombres);
        System.out.println(IntStream.rangeClosed(1, 5).map(x -> x * x).boxed().toList()
                + " promedio=" + IntStream.of(8, 9, 10).average().orElse(0));
        Function<Integer, Integer> doble = x -> x * 2;
        Predicate<String> vacio = String::isBlank;
        BiFunction<Integer, Integer, Integer> sumar = Integer::sum;
        Supplier<List<String>> nueva = ArrayList::new;
        System.out.println(doble.apply(4) + " " + vacio.test(" ") + " " + sumar.apply(2, 3) + " " + nueva.get());

        System.out.println("\n===== POO + POLIMORFISMO");
        List<Empleado> nomina = new ArrayList<>(List.of(new TiempoCompleto("Ana", 900), new PorHoras("Luis", 180, 5.5)));
        Collections.sort(nomina);                    // usa compareTo (mayor pago primero)
        nomina.forEach(System.out::println);
        System.out.printf("Total: %.2f | IESS Ana: %.2f%n", nomina.stream().mapToDouble(Pagable::calcularPago).sum(), nomina.get(0).aporteIess());
        Object obj = nomina.get(1);
        if (obj instanceof PorHoras ph) System.out.println("Pattern matching: " + ph.getNombre());   // Java 16+

        System.out.println("\n===== EXCEPCIONES");
        try {
            System.out.println("Quedan: " + vender(inventario, "P02", 2));
            vender(inventario, "P02", 50);
        } catch (StockInsuficienteException e) {
            System.out.println("Error: " + e.getMessage());
        } finally {
            System.out.println("finally siempre se ejecuta");
        }
        try { new Producto("X", "Gratis", 0, 1); } catch (IllegalArgumentException e) { System.out.println("record validó: " + e.getMessage()); }
        try { Integer.parseInt("abc"); } catch (NumberFormatException e) { System.out.println("NumberFormatException"); }
        try { int[] arr = new int[2]; arr[5] = 1; } catch (ArrayIndexOutOfBoundsException e) { System.out.println("Índice fuera de rango"); }
        String nulo = null;
        try { nulo.length(); } catch (NullPointerException e) { System.out.println("NullPointerException: usa Optional o verifica null"); }

        System.out.println("\n===== FECHAS (java.time)");
        LocalDate hoy = LocalDate.of(2026, 9, 25);
        LocalDate nacimiento = LocalDate.parse("2001-03-15");
        System.out.println(hoy.plusDays(30) + " edad=" + Period.between(nacimiento, hoy).getYears()
                + " " + hoy.getDayOfWeek() + " " + hoy.format(DateTimeFormatter.ofPattern("dd/MM/yyyy")));
        LocalTime ini = LocalTime.parse("08:00"), fin = LocalTime.parse("10:30");
        System.out.println("Duración: " + Duration.between(ini, fin).toMinutes() + " min, choca con 09:00-11:00: "
                + (ini.isBefore(LocalTime.parse("11:00")) && LocalTime.parse("09:00").isBefore(fin)));

        System.out.println("\n===== GENÉRICOS");
        System.out.println(maximo(List.of(3, 9, 4)) + " " + maximo(List.of("pera", "uva", "kiwi")));

        // Entrada por consola (descomenta):
        // Scanner sc = new Scanner(System.in);
        // System.out.print("Nombre: "); String nombre = sc.nextLine();
        // System.out.print("Edad: "); int edad = sc.nextInt(); sc.nextLine();   // consumir el Enter
    }
}
