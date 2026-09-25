# Sistema de Reserva de Laboratorios (Express)

Aplicación web para registrar laboratorios y gestionar sus reservas, evitando choques de horario.

## Funcionalidades
- CRUD de laboratorios (código único, piso, capacidad, estado).
- Reservas con validaciones: horario válido, laboratorio disponible y **sin cruces de horario**.
- Listado de reservas con filtros por fecha y laboratorio.
- Reporte de reservas y horas por laboratorio.
- API REST: `GET/POST /api/laboratorios`, `GET /api/reservas?fecha=AAAA-MM-DD`.

## Tecnologías
Node.js, Express, EJS, SQLite (better-sqlite3), HTML/CSS.

## Instalación y ejecución
```bash
npm install
npm run dev
```
Abrir http://localhost:3000. La base de datos `reservas.db` se crea automáticamente con 3 laboratorios de ejemplo.

## Pruebas
```bash
npm test
```

## Estructura
```
src/server.js          Punto de entrada
src/app.js             Configuración de Express
src/db/                Conexión y esquema SQL
src/validaciones.js    Reglas de negocio
src/routes/            Rutas (controladores) por módulo
views/                 Vistas EJS
public/css/            Estilos
test/                  Pruebas automáticas
```
