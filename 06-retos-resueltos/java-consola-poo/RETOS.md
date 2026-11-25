# Retos resueltos — Java

```bash
chcp 65001                              # Windows: tildes en consola
javac -encoding UTF-8 Biblioteca.java
java Biblioteca --test                  # 19 pruebas
java Biblioteca                         # menú con 14 opciones
```

## Reto 1: clase `Tesis` (3 días de préstamo)
- `class Tesis extends Material` con `autor` y `carrera`, y sobrescribe `diasPrestamo()` (3), `tipo()` y `toString()`.
- **Lección de polimorfismo:** no hubo que tocar `prestar()`. Calcula la fecha límite con `m.diasPrestamo()` y cada subclase responde lo suyo. Esto es el principio **Abierto/Cerrado** (SOLID): abierto a extensión, cerrado a modificación.

## Reto 2: guardar y cargar en CSV
- `guardarCsv(Path)`: encabezado + una línea por material con `Files.write(ruta, lineas, UTF_8)`. Cada subclase aporta sus columnas con `extraCsv()` (otra vez polimorfismo).
- `cargarCsv(Path)`: `Files.readAllLines` → `split(";", -1)` → `switch` sobre el tipo para crear el objeto correcto. Las líneas corruptas se **omiten y se cuentan** (try/catch por línea), así un error no tumba toda la carga.
- El constructor `Material(int id, ...)` conserva el id del archivo y ajusta el contador estático para que los nuevos ids no se repitan.
- `limpiar()` reemplaza `;` en los textos para no romper el formato.
- Opciones 13 y 14 del menú; al iniciar, carga `catalogo.csv` si existe.

## Reto 3: `Usuario` y préstamos
- `Usuario` valida la cédula (10 dígitos) y el nombre; se registran en un `Map<String, Usuario>` por cédula (búsqueda O(1)).
- `record Prestamo(material, usuario, desde, hasta)` es inmutable, con los métodos `diasAtraso(hoy)` y `multa(hoy)` ($0.25 por día).
- Reglas en `prestar()`: el material no puede estar prestado, máximo 3 préstamos por usuario, y no presta a quien tiene atrasos.
- `devolver()` retorna la multa. `atrasados(hoy)` lista los vencidos ordenados por fecha.
- Las fechas se reciben por parámetro (`LocalDate hoy`), así las pruebas pueden simular "dentro de 5 días" sin esperar.
- `eliminar()` ahora consulta el mapa de préstamos (ya no un booleano dentro de Material): cada responsabilidad queda en su lugar.
