# Biblioteca — Java en consola (POO + colecciones + streams)

Un solo archivo, sin dependencias. Menú CRUD con préstamos y estadísticas, y pruebas incluidas.

## Ejecutar (Java 17 o superior)
```bash
javac -encoding UTF-8 Biblioteca.java
java Biblioteca            # menú interactivo
java Biblioteca --test     # pruebas
```
Si las tildes se ven raras en la consola de Windows, ejecuta antes `chcp 65001`.

## Qué demuestra (y te pueden preguntar)
| Concepto | Dónde |
|---|---|
| Abstracción | `abstract class Material` con métodos abstractos |
| Herencia | `Libro extends Material`, `Revista extends Material` |
| Polimorfismo | `diasPrestamo()` y `toString()` distintos por clase |
| Encapsulamiento | campos `private` + getters/setters con validación |
| Interfaz | `implements Comparable<Material>` → `.sorted()` |
| Miembro static | `contador` para generar IDs |
| Excepción propia | `BibliotecaException extends Exception` |
| Colecciones | `LinkedHashMap`, `ArrayList`, `TreeMap` |
| Streams | `filter`, `sorted`, `groupingBy`, `counting`, `min`, `average` |
| Optional | `masAntiguo()` |
| Switch moderno | `case 1 -> ...` |
| Validación de entrada | `leerEntero()` con try/catch |

## Diferencias clave de Java
- `==` compara referencias; para textos usa `.equals()`.
- `ArrayList` (acceso rápido por índice) vs `LinkedList` (inserción rápida) vs `HashMap` (clave→valor, sin orden) vs `LinkedHashMap` (mantiene orden de inserción) vs `TreeMap` (ordenado).
- Checked exceptions (hay que declararlas/capturarlas, ej. `IOException`) vs unchecked (`RuntimeException`, ej. `IllegalArgumentException`).
- `interface` (solo contrato, múltiples) vs `abstract class` (puede tener estado, una sola).

## Reto para practicar
- Agregar la clase `Tesis extends Material` con 3 días de préstamo.
- Guardar y cargar el catálogo en un archivo CSV (`Files.writeString`, `Files.readAllLines`).
- Agregar una clase `Usuario` y registrar quién tiene cada préstamo.
