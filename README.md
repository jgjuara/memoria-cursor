# Sistema de Memoria para Agentes LLM

Una herramienta sencilla, liviana y portable para registrar información relevante del desarrollo de proyectos que puede alimentar las interacciones con agentes LLM (Cursor, Claude Code, etc.).

## 🚀 Instalación

### Como Módulo Python (Recomendado)

```bash
# Instalación desde PyPI (cuando esté disponible)
pip install memoria-cursor

# Instalación desde fuente
git clone https://github.com/jgjuara/memoria-cursor.git
cd memoria-cursor
pip install -e .

# Instalación usando uv (más rápido)
uv pip install git+https://github.com/jgjuara/memoria-cursor.git
```

## 🎯 Características

- **Sencillo y Liviano**: Sistema minimalista que no interfiere con el desarrollo
- **Portable**: Fácil de integrar en cualquier proyecto
- **Integración Git**: Captura automática de información de commits
- **Estructurado**: Entradas JSON con metadatos organizados
- **Herramientas Python**: Scripts para crear, listar y exportar entradas
- **Optimizado para LLM**: Exportación en formatos ideales para agentes IA

## 🚀 Instalación Rápida

### En un Nuevo Proyecto

```bash
# 1. Instalar el módulo (recomendado en venv)
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1
pip install -U pip
pip install memoria-cursor

# 2. Inicializar en tu proyecto
cd /path/to/tu-proyecto
memoria init --name "Nombre del Proyecto" --description "Descripción del proyecto"

# 3. Verificar instalación
memoria --help
```

## 📖 Uso Básico

### Crear una Entrada

```bash
# Registrar una decisión
memoria create decision "Elección de base de datos" "Se eligió PostgreSQL por su robustez" --tags "arquitectura" "base-datos"

# Registrar un cambio
memoria create change "Implementación de autenticación" "Sistema JWT agregado" --files auth.py --files models.py

# Registrar contexto
memoria create context "Configuración del entorno" "Python 3.8+, PostgreSQL 12+" --tags "configuracion"

# Registrar entrada relacionada con decisiones anteriores
memoria create change "Implementación de autenticación" "Sistema JWT basado en decisión anterior" --related-entries "550e8400-e29b-41d4-a716-446655440000" --tags "implementacion" "autenticacion"
```

### Listar Entradas

```bash
# Ver todas las entradas
memoria list

# Filtrar por tipo
memoria list --type decision

# Buscar por contenido
memoria list --search "postgresql"

# Ver estadísticas
memoria list --stats
```

### Exportar para LLM

```bash
# Exportar en Markdown (por defecto)
memoria export

# Exportar en JSON
memoria export --format json

# Exportar filtrando por tipo y etiquetas
memoria export --type decision --tags arquitectura --tags base-datos

# Exportar por rango de fechas y búsqueda de texto
memoria export --date-from 2025-01-01 --date-to 2025-12-31 --search "postgresql"

# Agrupar por tags
memoria export --group-by tags

# Chunking por tamaño aproximado (tokens ~ 4 chars)
memoria export --chunked --max-tokens 3000   # ~ 12k chars por archivo
memoria export --chunked --max-chars 12000   # límite directo por caracteres

# Resumen ejecutivo
memoria export --summary
```

## 🐍 Uso Programático (API Python)

### Importación e Inicialización

```python
from memoria_cursor import MemorySystem

# Crear instancia del sistema
m = MemorySystem('nombre-proyecto')

# Inicializar el proyecto (requerido antes de usar)
m.initialize_project()
```

### Crear Entradas Programáticamente

```python
# Crear una nota
entry_id = m.create_entry(
    'note',  # tipo: decision, change, context, bug, feature, note
    'Configuración inicial del proyecto',  # título
    'Se instaló memoria-cursor y se creó la documentación base...',  # contenido
    ['configuracion', 'memoria-cursor', 'documentacion']  # etiquetas
)

# Crear una decisión
decision_id = m.create_entry(
    'decision',
    'Elección de base de datos',
    'Se eligió PostgreSQL por su robustez ACID y soporte JSON nativo',
    ['arquitectura', 'base-datos', 'postgresql'],
    files_affected=['config/database.py', 'models/'],
    llm_context='Decisión de arquitectura que afecta toda la persistencia del sistema'
)
```

### Consultar y Filtrar Entradas

```python
# Obtener todas las entradas
entries = m.list_entries()

# Filtrar por tipo
decisions = m.list_entries(entry_type='decision')

# Buscar por etiquetas
config_entries = m.list_entries(tags=['configuracion'])

# Obtener entrada específica
entry = m.get_entry(entry_id)
```

### Exportar para LLM

```python
# Exportar en formato Markdown
m.export_entries()

# Exportar en formato JSON
m.export_entries(format='json')
```

### Parámetros del Método create_entry

- `entry_type` (str): Tipo de entrada (requerido)
- `title` (str): Título descriptivo (requerido)  
- `content` (str): Contenido principal (requerido)
- `tags` (List[str], opcional): Lista de etiquetas
- `files_affected` (List[str], opcional): Archivos afectados
- `llm_context` (str, opcional): Contexto específico para agentes LLM
- `related_entries` (List[str], opcional): IDs de entradas relacionadas

**Tipos de entrada válidos**: `decision`, `change`, `context`, `bug`, `feature`, `note`

## 📁 Estructura del Sistema

```
tu-proyecto/
├── entries/               # Entradas de memoria
├── export/                # Exportaciones para LLM
├── config/                # Configuración del sistema
└── MEMORIA.md             # Documentación del proyecto
```

## 🏗️ Tipos de Entradas

- **`decision`** - Decisiones de arquitectura y diseño
- **`change`** - Cambios importantes en el código
- **`context`** - Información de contexto del proyecto
- **`bug`** - Problemas y bugs encontrados
- **`feature`** - Nuevas funcionalidades implementadas
- **`note`** - Notas generales y observaciones

## 🔧 Integración con Git

El sistema captura automáticamente:
- Commit actual y mensaje
- Rama de trabajo
- Estado del repositorio (limpio/sucio)

Esta información se incluye en cada entrada para mejor trazabilidad.

## 🛠️ Desarrollo

### Instalación para Desarrollo

```bash
# Clonar repositorio
git clone https://github.com/jgjuara/memoria-cursor.git
cd memoria-cursor

# Instalar en modo desarrollo
pip install -e ".[dev]"

# Ejecutar pruebas
pytest

# Formatear código
black memoria_cursor/ tests/
```

### Estructura del Código

```
memoria_cursor/
├── core/                   # Funcionalidades principales
│   ├── entry.py           # Clase Entry
│   ├── memory_system.py   # Sistema principal
│   └── git_integration.py # Integración con Git
├── tools/                  # Herramientas de utilidad
│   ├── create.py          # Creación de entradas
│   ├── list.py            # Listado y búsqueda
│   └── export.py          # Exportación para LLM
├── config/                 # Configuración
│   ├── schema.json        # Esquema de validación
│   └── config.json        # Configuración del sistema
└── templates/              # Plantillas de entradas
    └── entry_templates.py # Plantillas predefinidas
```

## 📚 Documentación

- **[🚀 Guía para LLMs](docs/llm-guide.md)** - **Documentación específica para agentes LLM** ⭐
- **[📋 Plantillas para LLMs](docs/llm-templates.md)** - **Plantillas de código listas para usar** ⭐
- **[Guía de Uso](docs/guia-uso.md)** - Documentación completa
- **[Ejemplos](docs/ejemplos.md)** - Casos de uso prácticos
- **[API Python](docs/api-python.md)** - Documentación completa de la API Python
- **[Reglas para Agentes LLM](docs/reglas-agentes-llm.md)** - Instrucciones específicas para IA
- **[Estrategia de Integración](estrategia-integracion.md)** - Análisis de opciones de integración

## 🎯 Casos de Uso

### Para Desarrolladores
- Documentar decisiones de arquitectura
- Registrar cambios importantes en el código
- Mantener contexto del proyecto
- Facilitar onboarding de nuevos desarrolladores

### Para Agentes LLM
- Proporcionar contexto histórico del proyecto
- Compartir decisiones y razonamientos
- Facilitar continuidad en conversaciones
- Mejorar calidad de sugerencias y código

### Para Equipos
- Mantener conocimiento compartido
- Documentar lecciones aprendidas
- Facilitar code reviews informados
- Mejorar comunicación técnica

## 🔄 Migración desde bitacora.md

Si tienes un archivo `bitacora.md` existente:

1. Instalar el sistema de memoria
2. Migrar entradas importantes usando las herramientas
3. Mantener el archivo original como backup
4. Usar el nuevo sistema para futuras entradas

## 🤝 Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature
3. Implementar cambios
4. Agregar tests si es necesario
5. Enviar pull request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

- **Issues**: Reportar problemas en GitHub
- **Documentación**: Ver archivos en `docs/`
- **Ejemplos**: Ver `docs/ejemplos.md`

---

**¿Listo para mejorar la memoria de tus proyectos?** 🚀