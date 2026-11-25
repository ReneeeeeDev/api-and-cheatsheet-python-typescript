# Ejercicios de lógica (30) — intenta cada uno antes de ver la solución

Soluciones en `soluciones.py` y `soluciones.js` (mismas funciones, mismo orden).
Para comprobar tus propias respuestas, escribe tu función con el mismo nombre y ejecuta las pruebas:
`python soluciones.py` o `node soluciones.js`.

Tiempo sugerido: nivel 1 → 5 min c/u, nivel 2 → 10 min, nivel 3 → 15–20 min.

## Nivel 1 — Calentamiento
1. **es_par(n)**: devuelve True si n es par.
2. **mayor_de_tres(a, b, c)**: el mayor sin usar `max`.
3. **factorial(n)**: 5 → 120. Hazlo iterativo y recursivo.
4. **suma_digitos(n)**: 1234 → 10.
5. **invertir_texto(s)**: "hola" → "aloh" (sin `[::-1]` ni `reverse`).
6. **contar_vocales(s)**: "Murciélago" → 5 (considera tildes).
7. **tabla_multiplicar(n)**: lista con los 10 resultados de la tabla de n.
8. **celsius_a_fahrenheit(c)**: F = C × 9/5 + 32.
9. **es_bisiesto(anio)**: divisible para 4 y no para 100, o divisible para 400.
10. **fizzbuzz(n)**: lista de 1..n; múltiplos de 3 → "Fizz", de 5 → "Buzz", de ambos → "FizzBuzz".

## Nivel 2 — Lo más probable en la prueba
11. **es_primo(n)**: probar divisores hasta √n.
12. **fibonacci(n)**: lista con los primeros n términos: 7 → [0,1,1,2,3,5,8].
13. **es_palindromo(s)**: ignora espacios, mayúsculas y tildes. "Anita lava la tina" → True.
14. **contar_palabras(texto)**: diccionario palabra → veces (minúsculas, sin signos).
15. **segundo_mayor(lista)**: [4, 9, 9, 2] → 4 (valores distintos). None si no existe.
16. **eliminar_duplicados(lista)**: conservando el orden original.
17. **son_anagramas(a, b)**: "Roma", "amor" → True.
18. **mcd(a, b)** y **mcm(a, b)**: algoritmo de Euclides.
19. **decimal_a_binario(n)**: 10 → "1010" (sin `bin`).
20. **validar_cedula(cedula)**: cédula ecuatoriana (módulo 10). Algoritmo:
    - 10 dígitos; los 2 primeros = provincia (01–24 o 30); el tercero < 6.
    - Multiplica los 9 primeros por 2,1,2,1,2,1,2,1,2; si un producto > 9, réstale 9.
    - Suma todo; verificador = (10 − suma % 10) % 10; debe ser igual al 10.º dígito.
    - Válidas para probar: 1710034065, 0926687856.

## Nivel 3 — Para destacar
21. **busqueda_binaria(lista_ordenada, x)**: índice o -1. O(log n).
22. **ordenar_burbuja(lista)**: sin usar sort. Explica por qué es O(n²).
23. **parentesis_balanceados(s)**: "({[]})" → True, "([)]" → False. (Usa una pila.)
24. **comprimir(s)**: "aaabbc" → "a3b2c1".
25. **rotar_matriz(m)**: rotar una matriz cuadrada 90° a la derecha.
26. **dos_suma(nums, objetivo)**: índices de los 2 números que suman el objetivo, en O(n) con diccionario.
27. **numero_romano(n)**: 1994 → "MCMXCIV".
28. **agrupar_por(lista_dicts, clave)**: agrupa registros por un campo (típico de reportes).
29. **calcular_nomina(empleados)**: cada empleado tiene sueldo; el aporte IESS personal es 9.45 %; devuelve lista con nombre, aporte y neto (redondeado a 2 decimales), y el total neto.
30. **cajero(monto)**: menor cantidad de billetes/monedas (20, 10, 5, 1) para un monto entero. 38 → {20:1, 10:1, 5:1, 1:3}.

## Preguntas de razonamiento (responde en voz alta)
- ¿Qué complejidad tiene buscar en una lista vs en un diccionario/set? (O(n) vs O(1) promedio)
- ¿Cuándo usarías una pila y cuándo una cola?
- ¿Qué pasa si comparas `0.1 + 0.2 == 0.3`? ¿Cómo manejarías dinero? (float impreciso → usar enteros en centavos o `Decimal`)
- ¿Recursión vs iteración? (recursión más legible, pero usa la pila y puede desbordarse)
