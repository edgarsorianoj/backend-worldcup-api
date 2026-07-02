# 🏆 World Cup API

> Dashboard académico para visualizar las 48 selecciones clasificadas al Mundial de Fútbol 2026, consumiendo una API REST construida con **FastAPI** y un frontend minimalista en **HTML + CSS + JavaScript vanilla** con **Axios**.

---

## 📑 Tabla de contenidos

1. [Descripción del proyecto](#-descripción-del-proyecto)
2. [Tecnologías utilizadas](#-tecnologías-utilizadas)
3. [Estructura del proyecto](#-estructura-del-proyecto)
4. [Instalación en local](#-instalación-en-local)
5. [Configuración del entorno](#-configuración-del-entorno)
6. [Ejemplos de uso](#-ejemplos-de-uso)
7. [Capturas de pantalla](#-capturas-de-pantalla)
8. [Documentación de endpoints](#-documentación-de-endpoints)
9. [Arquitectura del backend](#-arquitectura-del-backend)
10. [Roadmap / posibles mejoras](#-roadmap--posibles-mejoras)

---

## 📖 Descripción del proyecto

**World Cup API** es un proyecto académico full-stack con foco en la correcta separación de capas y consumo de una API REST.

- **Backend**: API REST en Python con FastAPI que persiste selecciones nacionales en una base de datos SQLite mediante SQLModel (SQLAlchemy + Pydantic). Sigue una arquitectura por capas (domain / application / infrastructure) con repositorio abstracto e inyección de dependencias.
- **Frontend**: Dashboard de una sola página, sin frameworks, con tema oscuro minimalista, consumo **exclusivo con Axios** (sin `fetch`), animaciones, estados de carga, búsqueda, filtros y atajos de teclado.

El frontend renderiza dinámicamente las selecciones en tarjetas con su bandera (vía `flagcdn.com`), confederación, capitán, director técnico y palmarés de mundiales ganados.

---

## 🛠️ Tecnologías utilizadas

### Backend
| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.12+ | Lenguaje principal |
| FastAPI | 0.138.2 | Framework HTTP |
| Uvicorn | 0.49.0 | Servidor ASGI |
| SQLModel | 0.0.39 | ORM (SQLAlchemy + Pydantic) |
| SQLite | — | Base de datos embebida |
| Pydantic | (vía SQLModel) | Validación de payloads |
| validators | (vía seed) | Validación de URLs |
| pytest | 8.4.2 | Tests |
| httpx | 0.28.1 | Cliente HTTP para tests |

### Frontend
| Tecnología | Versión | Uso |
|---|---|---|
| HTML5 | — | Estructura semántica |
| CSS3 | — | Estilos, animaciones, responsive |
| JavaScript | ES2020+ | Lógica de UI (vanilla) |
| Axios | 1.7.7 | Cliente HTTP (vía CDN) |
| Inter | — | Tipografía principal (Google Fonts) |
| flagcdn.com | — | Banderas SVG externas |

---

## 📁 Estructura del proyecto

```
world-cup-api/
├── backend/
│   ├── conftest.py
│   ├── main.py                    # Entry point FastAPI + CORS
│   ├── requirements.txt
│   ├── seed.py                    # Carga 48 selecciones iniciales
│   ├── selections.db              # SQLite (ignorado por git)
│   └── src/
│       └── selections/
│           ├── application/       # Casos de uso (CQRS ligero)
│           │   ├── create_selection.py
│           │   ├── delete_selection.py
│           │   ├── get_all_selections.py
│           │   ├── get_selection_by_id.py
│           │   └── update_selection.py
│           ├── domain/            # Entidades, VO, errores, contratos
│           │   ├── exception.py
│           │   ├── models.py
│           │   ├── repositories.py
│           │   └── value_objects.py
│           ├── infraestructure/   # Adaptadores (FastAPI router + repo SQLModel)
│           │   ├── api.py
│           │   └── repositories.py
│           └── test/              # Tests unitarios
└── frontend/
    ├── index.html                 # Estructura HTML semántica
    ├── styles.css                 # Tema oscuro minimalista + animaciones
    └── main.js                    # Lógica UI + Axios
```

---

## ⚙️ Instalación en local

### Requisitos previos
- **Python 3.12+**
- **pip**
- Un navegador moderno (Chrome, Firefox, Edge, Safari)
- (Opcional) **VS Code** con la extensión *Live Server* o cualquier servidor estático

### 1. Clonar el repositorio
```bash
git clone <url-del-repo>
cd world-cup-api
```

### 2. Crear y activar el entorno virtual
```bash
cd backend
python -m venv ../.venv
```

**Linux / macOS**
```bash
source ../.venv/bin/activate
```

**Windows (PowerShell)**
```powershell
..\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias del backend
```bash
pip install -r requirements.txt
```

### 4. Sembrar la base de datos (opcional pero recomendado)
Carga las 48 selecciones del Mundial 2026:
```bash
python seed.py
```
Salida esperada: `Database seeded successfully`

### 5. Levantar el backend
```bash
uvicorn main:app --reload
```
La API quedará disponible en `http://127.0.0.1:8000`.

- Documentación interactiva Swagger: <http://127.0.0.1:8000/docs>
- Documentación alternativa ReDoc: <http://127.0.0.1:8000/redoc>

### 6. Abrir el frontend
Opción A — **directo en el navegador** (la más simple):
```bash
# Desde la carpeta frontend/
xdg-open index.html   # Linux
open index.html       # macOS
start index.html      # Windows
```

Opción B — **con servidor estático** (recomendado para evitar restricciones de CORS/file://):
```bash
# Si tenés Python
cd frontend
python -m http.server 5500
# Abrí http://127.0.0.1:5500
```

Opción C — **VS Code Live Server**:
1. Instalá la extensión *Live Server*.
2. Click derecho sobre `frontend/index.html` → *Open with Live Server*.

---

## 🔧 Configuración del entorno

### Backend
No requiere variables de entorno. La URL base de la API es `http://127.0.0.1:8000` por defecto.

Si necesitás cambiar el host o puerto:
```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Frontend
La URL de la API está definida en `frontend/main.js`:

```js
const API_BASE_URL = 'http://127.0.0.1:8000';
```

Si modificás el puerto del backend, editá esa constante. El frontend **debe** ser capaz de alcanzar esa URL (verificá la consola con F12 → *Network* si hay errores CORS).

### CORS
El backend tiene CORS abierto para todos los orígenes (`allow_origins=["*"]`), pensado para uso académico. En producción se debería restringir a dominios concretos.

---

## 💡 Ejemplos de uso

### 1. Listar todas las selecciones
```bash
curl http://127.0.0.1:8000/selections/
```

### 2. Obtener una selección por ID
```bash
curl http://127.0.0.1:8000/selections/1
```

Respuesta:
```json
{
  "id": 1,
  "country": "Spain",
  "confederation": "UEFA",
  "captain": "Rodri",
  "coach": "Luis de la Fuente",
  "world_cups": 1,
  "flag": "https://flagcdn.com/es.svg"
}
```

### 3. Crear una nueva selección
```bash
curl -X POST http://127.0.0.1:8000/selections/ \
  -H "Content-Type: application/json" \
  -d '{
    "country": "Japan",
    "confederation": "AFC",
    "captain": "Wataru Endo",
    "coach": "Hajime Moriyasu",
    "world_cups": 0,
    "flag": "https://flagcdn.com/jp.svg"
  }'
```

### 4. Actualizar una selección existente
```bash
curl -X PUT http://127.0.0.1:8000/selections/1 \
  -H "Content-Type: application/json" \
  -d '{
    "country": "Spain",
    "confederation": "UEFA",
    "captain": "Rodri",
    "coach": "Luis de la Fuente",
    "world_cups": 2,
    "flag": "https://flagcdn.com/es.svg"
  }'
```

### 5. Eliminar una selección
```bash
curl -X DELETE http://127.0.0.1:8000/selections/1
```
Retorna `204 No Content`.

### 6. Consumir la API desde el frontend
```js
// Ejemplo: fetch con Axios (única forma permitida en el proyecto)
axios.get('http://127.0.0.1:8000/selections')
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

### 7. Atajos de teclado del frontend
| Tecla | Acción |
|---|---|
| `/` | Enfocar la búsqueda |
| `R` | Recargar selecciones |
| `Enter` / `Espacio` (sobre tarjeta) | Abrir detalle |
| `Esc` | Cerrar modal, menú móvil o panel de atajos |
| `?` | Mostrar panel de atajos |

---

## 📸 Capturas de pantalla

> ⚠️ **No es posible generar capturas en este entorno.** A continuación, la lista de pantallas que **te recomiendo capturar** manualmente para incluirlas en el README. Para tomarlas, levantá el proyecto (backend + frontend) y hacé las acciones indicadas.

### Capturas sugeridas

| # | Pantalla | Qué deberías capturar |
|---|---|---|
| 1 | **Hero y métricas** | Vista inicial con el título "Selecciones clasificadas", el badge "En vivo · Temporada 2026" y los 4 stats (Selecciones / Confederaciones / Campeones / Actualizado). |
| 2 | **Grid de tarjetas cargado** | Vista con las 48 tarjetas renderizadas mostrando banderas, confederación, capitán, DT y trofeos. Idealmente con la primera tarjeta en hover para mostrar el efecto de elevación + flecha. |
| 3 | **Búsqueda con resultados** | Escribí "bra" en el buscador para filtrar Brasil (y cualquier coincidencia), y que se vea el chip "bra" + el contador "1 / 48". |
| 4 | **Filtro por confederación** | Seleccioná "UEFA" en el dropdown y capturá el grid filtrado con el chip "UEFA" visible arriba. |
| 5 | **Tarjeta en hover** | Acercate a una tarjeta con el mouse para mostrar la flecha cyan apareciendo y el ligero translateY. |
| 6 | **Modal de detalle** | Hacé click en cualquier tarjeta (o presioná Enter) y capturá el modal con bandera, capitán, DT y mundiales ganados. |
| 7 | **Estado de error** | Apagá el backend (`Ctrl+C` en la terminal) y hacé click en "Reintentar" para capturar la pantalla de error con borde rojo y mensaje. |
| 8 | **Estado de carga (skeleton)** | Con el backend apagado o con throttling de red, recargá la página para capturar los skeletons con shimmer antes de que aparezca el error. |
| 9 | **Toast de feedback** | Capturá un toast (por ejemplo, después de "Recargar" exitoso) deslizándose desde la esquina inferior derecha. |
| 10 | **Panel de atajos** | Pulsá `?` y capturá el panel superpuesto con los atajos. |
| 11 | **Vista móvil** | Redimensioná la ventana a ~400px de ancho o usá las DevTools (F12 → modo responsive) y capturá: menú hamburguesa abierto, grid en una columna, stats en columna. |
| 12 | **Backend Swagger** | Visitá `http://127.0.0.1:8000/docs` y capturá la documentación interactiva de FastAPI. |

### Cómo incluir las capturas

1. Guardá las imágenes en una carpeta `docs/screenshots/` en la raíz del proyecto.
2. Usá un nombre descriptivo: `01-hero.png`, `02-grid-completo.png`, etc.
3. Insertalas en este README con Markdown:

```markdown
![Hero y métricas](docs/screenshots/01-hero.png)
![Grid completo](docs/screenshots/02-grid-completo.png)
```

---

## 📡 Documentación de endpoints

**Base URL**: `http://127.0.0.1:8000`

> ℹ️ El router está montado con `prefix="/selections"`. Todas las rutas de selección cuelgan de ese prefijo.

### Endpoints disponibles

| Método | Ruta | Descripción | Status |
|---|---|---|---|
| `GET` | `/` | Endpoint raíz — mensaje de bienvenida | 200 |
| `GET` | `/selections/` | Lista todas las selecciones | 200 |
| `GET` | `/selections/{id}` | Obtiene una selección por ID | 200 / 404 |
| `POST` | `/selections/` | Crea una nueva selección | 201 / 400 |
| `PUT` | `/selections/{id}` | Actualiza una selección existente | 200 / 404 / 400 |
| `DELETE` | `/selections/{id}` | Elimina una selección | 204 / 404 |

---

### `GET /`
Devuelve un mensaje de bienvenida.

**Respuesta**:
```json
{
  "msg": "World Cup 2026 API"
}
```

---

### `GET /selections/`
Devuelve el listado completo de selecciones.

**Respuesta 200**:
```json
[
  {
    "id": 1,
    "country": "Spain",
    "confederation": "UEFA",
    "captain": "Rodri",
    "coach": "Luis de la Fuente",
    "world_cups": 1,
    "flag": "https://flagcdn.com/es.svg"
  },
  {
    "id": 2,
    "country": "Argentina",
    "confederation": "CONMEBOL",
    "captain": "Lionel Messi",
    "coach": "Lionel Scaloni",
    "world_cups": 3,
    "flag": "https://flagcdn.com/ar.svg"
  }
]
```

---

### `GET /selections/{id}`
Devuelve una selección por su identificador.

**Parámetros**:
- `id` (path, requerido): identificador numérico entero.

**Respuesta 200**:
```json
{
  "id": 1,
  "country": "Spain",
  "confederation": "UEFA",
  "captain": "Rodri",
  "coach": "Luis de la Fuente",
  "world_cups": 1,
  "flag": "https://flagcdn.com/es.svg"
}
```

**Respuesta 404** (no existe):
```json
{
  "detail": "Selection not found"
}
```

---

### `POST /selections/`
Crea una nueva selección.

**Body (JSON)**:
```json
{
  "country": "Japan",
  "confederation": "AFC",
  "captain": "Wataru Endo",
  "coach": "Hajime Moriyasu",
  "world_cups": 0,
  "flag": "https://flagcdn.com/jp.svg"
}
```

**Campos del payload**:
| Campo | Tipo | Requerido | Validación |
|---|---|---|---|
| `country` | string | ✅ | — |
| `confederation` | string | ✅ | — |
| `captain` | string | ✅ | — |
| `coach` | string | ✅ | — |
| `world_cups` | integer | ✅ | — |
| `flag` | string (URL) | ✅ | Debe ser una URL válida (validators.url) |

**Respuesta 201**:
```json
{
  "id": 49,
  "country": "Japan",
  "confederation": "AFC",
  "captain": "Wataru Endo",
  "coach": "Hajime Moriyasu",
  "world_cups": 0,
  "flag": "https://flagcdn.com/jp.svg"
}
```

**Respuesta 400** (URL inválida):
```json
{
  "detail": "Invalid flag URL"
}
```

---

### `PUT /selections/{id}`
Actualiza completamente una selección existente (no parcial).

**Parámetros**:
- `id` (path, requerido): identificador numérico entero.

**Body (JSON)**: misma estructura que `POST`.

**Respuesta 200**: objeto actualizado.

**Respuesta 404**: `{ "detail": "Selection not found" }`

**Respuesta 400**: `{ "detail": "Invalid flag URL" }`

---

### `DELETE /selections/{id}`
Elimina una selección por su ID.

**Parámetros**:
- `id` (path, requerido): identificador numérico entero.

**Respuesta 204** (sin contenido).

**Respuesta 404** (no existe):
```json
{
  "detail": "Selection not found"
}
```

---

### Errores comunes
| Código | Causa |
|---|---|
| `400 Bad Request` | URL de la bandera inválida. |
| `404 Not Found` | ID de selección inexistente. |
| `422 Unprocessable Entity` | Body con tipos o campos faltantes. |

---

## 🏛️ Arquitectura del backend

El backend sigue una **arquitectura por capas** con dependencias unidireccionales:

```
┌──────────────────────────────┐
│  infraestructure/api.py      │  ← FastAPI router (adaptador)
└──────────────┬───────────────┘
               │ usa
               ▼
┌──────────────────────────────┐
│  application/                │  ← Casos de uso
│   - create_selection         │     (orquestación, comandos)
│   - update_selection         │
│   - delete_selection         │
│   - get_all_selections       │
│   - get_selection_by_id      │
└──────────────┬───────────────┘
               │ depende de la abstracción
               ▼
┌──────────────────────────────┐
│  domain/                     │  ← Núcleo
│   - models.py (Selection)    │     (entidades, VO, contratos)
│   - value_objects.py         │
│   - repositories.py (ABC)    │
│   - exception.py             │
└──────────────┬───────────────┘
               │ implementado por
               ▼
┌──────────────────────────────┐
│  infraestructure/            │
│   repositories.py (SQLModel) │  ← Adaptador de persistencia
└──────────────────────────────┘
```

**Ventajas**:
- El dominio no conoce FastAPI ni SQLModel: sólo Python puro.
- Cambiar la persistencia (a Postgres, por ejemplo) sólo requiere un nuevo adaptador que implemente `SelectionRepository`.
- Los casos de uso son fácilmente testables con un *mock* del repositorio.

---

## 🧪 Tests

Para correr los tests del backend:
```bash
cd backend
pytest
```

Los tests viven en `backend/src/selections/test/` y cubren los casos de uso de la capa de aplicación.

---

## 🗺️ Roadmap / posibles mejoras

- [ ] Endpoint adicional `GET /selections/confederation/{confederation}` para filtrar por confederación desde el backend (actualmente el filtrado se hace en el frontend).
- [ ] Endpoint adicional `GET /selections/country/{country}` para búsqueda por país.
- [ ] Paginación (`?limit=&offset=`) cuando crezca el dataset.
- [ ] Autenticación con JWT para `POST`, `PUT` y `DELETE`.
- [ ] Migración de SQLite a PostgreSQL para producción.
- [ ] Modo claro (light mode) con `prefers-color-scheme` (la paleta ya está invertida y lista para activarse desde CSS).
- [ ] Internacionalización (i18n) del frontend.

---

## 📄 Licencia

Proyecto académico sin licencia específica. Usar libremente con fines educativos.

---

**Hecho con ⚽ para la comunidad académica.**
