# Cheatsheet Git + GitHub

## Configuración inicial (en la PC del laboratorio, lo primero)

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
git config --list
```

## Flujo básico

```bash
git init                         # crea repo en la carpeta actual
git status                       # qué cambió (úsalo todo el tiempo)
git add archivo.py               # prepara un archivo
git add .                        # prepara todo
git commit -m "feat: agregar CRUD de productos"
git log --oneline --graph        # historial compacto
git diff                         # cambios sin preparar
```

## Remoto (GitHub)

```bash
git remote add origin https://github.com/usuario/repo.git
git branch -M main
git push -u origin main          # la primera vez
git push                         # siguientes veces
git pull                         # traer cambios
git clone https://github.com/usuario/repo.git
```

GitHub ya no acepta contraseña por HTTPS: usa un **Personal Access Token** (Settings → Developer settings → Tokens) como contraseña, o inicia sesión con `gh auth login` / GitHub Desktop.

## Ramas

```bash
git branch                       # listar
git switch -c feature/login      # crear y cambiar (antiguo: git checkout -b)
git switch main                  # cambiar
git merge feature/login          # unir la rama a la actual
git branch -d feature/login      # borrar rama
```

### Resolver un conflicto
1. `git merge rama` → "CONFLICT".
2. Abre el archivo, verás:
   ```
   <<<<<<< HEAD
   tu versión
   =======
   la otra versión
   >>>>>>> rama
   ```
3. Deja el código correcto, borra las marcas.
4. `git add archivo` → `git commit`.

## Deshacer cosas

```bash
git restore archivo              # descartar cambios no guardados
git restore --staged archivo     # sacar del staging
git commit --amend -m "nuevo msg" # corregir el último commit (si no hiciste push)
git reset --soft HEAD~1          # deshacer último commit, conservar cambios
git revert <hash>                # commit que invierte otro (seguro si ya hiciste push)
git stash / git stash pop        # guardar cambios temporalmente
```

## .gitignore típico

```
node_modules/
venv/
__pycache__/
.env
*.db
dist/
build/
.vscode/
target/
*.class
```

## Buenas prácticas (que el evaluador nota)

- Commits pequeños y frecuentes con mensajes claros:
  `feat: ...` (nueva función), `fix: ...` (corrección), `docs: ...`, `style: ...`, `refactor: ...`, `test: ...`
- Nunca subir `node_modules`, `venv`, contraseñas ni `.env`.
- README.md con: descripción, requisitos, cómo instalar y ejecutar, capturas.

## Preguntas teóricas típicas

- **Git vs GitHub**: Git es el sistema de control de versiones (local); GitHub es un servicio que aloja repositorios remotos.
- **merge vs rebase**: merge une historias creando un commit de unión; rebase reescribe la historia poniendo tus commits encima (historial lineal). No hacer rebase de ramas compartidas.
- **fetch vs pull**: fetch descarga sin mezclar; pull = fetch + merge.
- **Pull Request**: solicitud para revisar e integrar una rama en otra.
- **Staging area**: zona intermedia entre tus cambios y el commit (`git add`).

---

# PARTE 2 — AMPLIACIÓN

## Modelo mental: las 3 zonas + remoto

```
 Directorio de trabajo ──git add──►  Staging (índice) ──git commit──►  Repositorio local ──git push──►  GitHub (remoto)
        ▲                                                                     │                               │
        └──────────────── git restore / checkout ◄────────────────────────────┘ ◄──────── git pull / fetch ───┘
```

## Ejercicio práctico completo (hazlo en 10 minutos)

```bash
mkdir practica-git && cd practica-git
git init
echo "# Mi proyecto" > README.md
git add README.md
git commit -m "docs: README inicial"

git switch -c feature/saludo            # nueva rama
echo "print('hola')" > app.py
git add . && git commit -m "feat: saludo"

git switch main
echo "Versión 1" >> README.md
git commit -am "docs: versión"          # -a solo sirve para archivos ya rastreados

git merge feature/saludo                 # une la rama (merge commit)
git log --oneline --graph --all          # ver el árbol

# Provocar un conflicto
git switch -c rama-a && echo "A" > conflicto.txt && git add . && git commit -m "A"
git switch main && echo "B" > conflicto.txt && git add . && git commit -m "B"
git merge rama-a                         # CONFLICT → edita conflicto.txt, deja lo correcto
git add conflicto.txt && git commit -m "merge: resolver conflicto"
```

## Comandos de consulta

```bash
git log --oneline -10                    # últimos 10
git log --author="Ana" --since="2 days ago"
git log -p archivo.py                    # cambios de un archivo
git show <hash>                          # detalle de un commit
git diff main..feature/login             # diferencias entre ramas
git diff --staged                        # lo que va en el próximo commit
git blame archivo.py                     # quién cambió cada línea
git branch -a                            # ramas locales y remotas
git remote -v                            # ver remotos
git status -s                            # estado corto
```

## Deshacer: guía rápida según la situación

| Situación | Comando |
|---|---|
| Modifiqué un archivo y quiero volver a como estaba | `git restore archivo` |
| Hice `git add` de algo por error | `git restore --staged archivo` |
| El último commit tiene un error en el mensaje (sin push) | `git commit --amend -m "mensaje correcto"` |
| Olvidé agregar un archivo al último commit (sin push) | `git add olvidado && git commit --amend --no-edit` |
| Deshacer el último commit conservando los cambios | `git reset --soft HEAD~1` |
| Deshacer el último commit y **borrar** los cambios | `git reset --hard HEAD~1` (¡peligroso!) |
| Ya hice push y quiero revertir un commit | `git revert <hash>` (crea un commit inverso) |
| Quiero guardar mis cambios un momento y cambiar de rama | `git stash` → cambiar → volver → `git stash pop` |
| Subí `node_modules` por error | Agregarlo a `.gitignore`, `git rm -r --cached node_modules`, commit |
| Recuperar algo "perdido" tras un reset | `git reflog` → `git reset --hard <hash>` |

## Flujo de trabajo en equipo (GitHub Flow)

1. `git pull` en main para estar actualizado.
2. `git switch -c feature/nombre-descriptivo`.
3. Commits pequeños.
4. `git push -u origin feature/nombre-descriptivo`.
5. En GitHub: **Pull Request** → revisión de código → aprobar → **Merge**.
6. `git switch main && git pull && git branch -d feature/...`.

**Git Flow** (más formal): ramas `main` (producción), `develop` (integración), `feature/*`, `release/*`, `hotfix/*`.

## Rebase y cherry-pick

```bash
git switch feature/login
git rebase main                   # reaplica tus commits encima de main (historial lineal)
# conflicto → resolver → git add . → git rebase --continue   (o git rebase --abort)
git cherry-pick <hash>            # copia UN commit de otra rama a la actual
```
**Regla:** nunca hagas rebase de commits que ya subiste y que otros usan.

## Etiquetas (versiones)

```bash
git tag -a v1.0.0 -m "Primera versión"
git push origin v1.0.0
```
Versionado semántico **MAJOR.MINOR.PATCH**: 2.0.0 trae cambios incompatibles, 1.3.0 una nueva función compatible y 1.2.1 una corrección.

## Autenticación con GitHub

- **HTTPS + token:** GitHub → Settings → Developer settings → Personal access tokens → Generate (scope `repo`). Al hacer push, en "password" pegas el token.
- **GitHub CLI:** `gh auth login` → sigue los pasos en el navegador.
- **SSH:** `ssh-keygen -t ed25519 -C "tu@correo.com"` → copia `~/.ssh/id_ed25519.pub` en GitHub → SSH keys → usa la URL `git@github.com:usuario/repo.git`.
- En una PC ajena (laboratorio), **al terminar** cierra sesión: Panel de control → Administrador de credenciales → Credenciales de Windows → borra `git:https://github.com`.

## Convención de commits (Conventional Commits)

```
tipo(ámbito opcional): descripción en imperativo y minúscula

feat: agregar filtro por fecha en reservas
fix(api): devolver 404 cuando el laboratorio no existe
docs: instrucciones de instalación en README
style: formatear con prettier
refactor: extraer validaciones a módulo aparte
test: pruebas de choque de horarios
chore: actualizar dependencias
```

## CI con GitHub Actions (ejecutar pruebas en cada push)

`.github/workflows/pruebas.yml`:
```yaml
name: Pruebas
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: python -m unittest discover tests -v
```
Para Node: `actions/setup-node@v4` con `node-version: 22`, luego `npm ci` y `npm test`.
