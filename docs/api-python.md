# API Python - Sistema de Memoria para Agentes LLM

## Descripción General

Este documento describe la API Python del módulo `memoria-cursor`, que permite usar el sistema de memoria programáticamente desde código Python. Esta API es especialmente útil para:

- Scripts de automatización
- Integración en herramientas de desarrollo
- Uso por agentes LLM
- Workflows personalizados

## Importación e Inicialización

### Importar el Módulo

```python
from memoria_cursor import MemorySystem
```

### Crear Instancia del Sistema

```python
# Crear instancia del sistema
m = MemorySystem('nombre-proyecto')

# Inicializar el proyecto (REQUERIDO antes de usar otros métodos)
m.initialize_project()
```

**Nota crítica**: Siempre debes llamar `initialize_project()` antes de usar cualquier otro método. Este método:
- Crea la estructura de directorios necesaria
- Inicializa archivos de configuración
- Configura la integración con Git si está disponible

## Clase MemorySystem

### Constructor

```python
MemorySystem(project_name: str, config_dir: Optional[str] = None)
```

**Parámetros**:
- `project_name` (str): Nombre del proyecto (requerido)
- `config_dir` (str, opcional): Directorio de configuración personalizado

### Métodos Principales

#### initialize_project()

Inicializa el sistema de memoria en el proyecto.

```python
def initialize_project(self) -> None
```

**Comportamiento**:
- Crea directorios: `config/`, `entries/`, `export/`
- Inicializa archivos de configuración
- Configura integración Git si está disponible
- Crea archivo `.gitignore` si no existe

#### create_entry()

Crea una nueva entrada en el sistema de memoria.

```python
def create_entry(
    self,
    entry_type: str,                    # Tipo de entrada (requerido)
    title: str,                         # Título descriptivo (requerido)
    content: str,                       # Contenido principal (requerido)
    tags: Optional[List[str]] = None,   # Etiquetas opcionales
    files_affected: Optional[List[str]] = None,  # Archivos afectados opcionales
    llm_context: Optional[str] = None,  # Contexto para LLM opcional
    related_entries: Optional[List[str]] = None  # Entradas relacionadas opcionales
) -> str
```

**Parámetros**:
- `entry_type` (str): Tipo de entrada. Debe ser uno de:
  - `'decision'` - Decisiones de arquitectura y diseño
  - `'change'` - Cambios importantes en el código
  - `'context'` - Información de contexto del proyecto
  - `'bug'` - Problemas y bugs encontrados
  - `'feature'` - Nuevas funcionalidades implementadas
  - `'note'` - Notas generales y observaciones

- `title` (str): Título descriptivo de la entrada
- `content` (str): Contenido principal de la entrada
- `tags` (List[str], opcional): Lista de etiquetas para categorización
- `files_affected` (List[str], opcional): Lista de archivos afectados por el cambio
- `llm_context` (str, opcional): Información específica para agentes LLM
- `related_entries` (List[str], opcional): Lista de IDs de entradas relacionadas

**Retorna**: ID único de la entrada creada (str)

**Ejemplo**:
```python
entry_id = m.create_entry(
    'decision',
    'Elección de base de datos',
    'Se eligió PostgreSQL por su robustez ACID y soporte JSON nativo.',
    ['arquitectura', 'base-datos', 'postgresql'],
    files_affected=['config/database.py', 'models/'],
    llm_context='Decisión fundamental que afecta toda la arquitectura de persistencia'
)
```

#### list_entries()

Lista entradas con filtros opcionales.

```python
def list_entries(
    self,
    limit: Optional[int] = None,           # Número máximo de entradas
    entry_type: Optional[str] = None,      # Filtrar por tipo
    tags: Optional[List[str]] = None,      # Filtrar por etiquetas
    search: Optional[str] = None,          # Buscar en título y contenido
    date_from: Optional[str] = None,       # Fecha de inicio (YYYY-MM-DD)
    date_to: Optional[str] = None          # Fecha de fin (YYYY-MM-DD)
) -> List[Entry]
```

**Parámetros**:
- `limit` (int, opcional): Número máximo de entradas a retornar
- `entry_type` (str, opcional): Filtrar por tipo de entrada
- `tags` (List[str], opcional): Filtrar por etiquetas (OR lógico)
- `search` (str, opcional): Buscar texto en título y contenido
- `date_from` (str, opcional): Fecha de inicio en formato YYYY-MM-DD
- `date_to` (str, opcional): Fecha de fin en formato YYYY-MM-DD

**Retorna**: Lista de objetos Entry

**Ejemplos**:
```python
# Obtener todas las entradas
all_entries = m.list_entries()

# Filtrar por tipo
decisions = m.list_entries(entry_type='decision')

# Buscar por etiquetas
arch_entries = m.list_entries(tags=['arquitectura'])

# Búsqueda de texto
postgres_entries = m.list_entries(search='postgresql')

# Combinar filtros
recent_decisions = m.list_entries(
    entry_type='decision',
    limit=5,
    tags=['arquitectura']
)
```

#### get_entry()

Obtiene una entrada específica por ID.

```python
def get_entry(self, entry_id: str) -> Optional[Entry]
```

**Parámetros**:
- `entry_id` (str): ID de la entrada a buscar

**Retorna**: Objeto Entry o None si no se encuentra

**Ejemplo**:
```python
entry = m.get_entry('550e8400-e29b-41d4-a716-446655440000')
if entry:
    print(f"Título: {entry.title}")
    print(f"Tipo: {entry.entry_type}")
    print(f"Contenido: {entry.content}")
```

#### update_entry()

Actualiza una entrada existente.

```python
def update_entry(
    self,
    entry_id: str,
    title: Optional[str] = None,
    content: Optional[str] = None,
    tags: Optional[List[str]] = None,
    files_affected: Optional[List[str]] = None,
    llm_context: Optional[str] = None,
    related_entries: Optional[List[str]] = None
) -> bool
```

**Parámetros**:
- `entry_id` (str): ID de la entrada a actualizar
- `title` (str, opcional): Nuevo título
- `content` (str, opcional): Nuevo contenido
- `tags` (List[str], opcional): Nuevas etiquetas
- `files_affected` (List[str], opcional): Nuevos archivos afectados
- `llm_context` (str, opcional): Nuevo contexto LLM
- `related_entries` (List[str], opcional): Nuevas entradas relacionadas

**Retorna**: True si se actualizó correctamente, False en caso contrario

**Ejemplo**:
```python
success = m.update_entry(
    entry_id,
    title='Título actualizado',
    content='Contenido actualizado',
    tags=['nueva', 'etiqueta']
)
```

#### delete_entry()

Elimina una entrada del sistema.

```python
def delete_entry(self, entry_id: str) -> bool
```

**Parámetros**:
- `entry_id` (str): ID de la entrada a eliminar

**Retorna**: True si se eliminó correctamente, False en caso contrario

**Ejemplo**:
```python
success = m.delete_entry('550e8400-e29b-41d4-a716-446655440000')
```

#### export_entries()

Exporta las entradas en formatos legibles para LLM.

```python
def export_entries(
    self,
    format: str = 'markdown',
    entry_type: Optional[str] = None,
    tags: Optional[List[str]] = None,
    search: Optional[str] = None
) -> str
```

**Parámetros**:
- `format` (str): Formato de exportación ('markdown' o 'json')
- `entry_type` (str, opcional): Exportar solo entradas de un tipo
- `tags` (List[str], opcional): Exportar solo entradas con etiquetas específicas
- `search` (str, opcional): Exportar solo entradas que coincidan con búsqueda

**Retorna**: Ruta del archivo exportado

**Ejemplos**:
```python
# Exportar todas las entradas en Markdown
m.export_entries()

# Exportar solo decisiones en JSON
m.export_entries(format='json', entry_type='decision')

# Exportar entradas relacionadas con arquitectura
m.export_entries(tags=['arquitectura'])
```

#### get_statistics()

Obtiene estadísticas del sistema de memoria.

```python
def get_statistics(self) -> Dict[str, Any]
```

**Retorna**: Diccionario con estadísticas del sistema

**Ejemplo**:
```python
stats = m.get_statistics()
print(f"Total de entradas: {stats['total_entries']}")
print(f"Última actualización: {stats['last_updated']}")
print(f"Tipos de entrada: {stats['entry_types']}")
```

### Propiedades

#### project_root
Ruta al directorio raíz del proyecto.

#### config_dir
Ruta al directorio de configuración.

#### entries_dir
Ruta al directorio de entradas.

#### export_dir
Ruta al directorio de exportación.

#### auto_git
Indica si la integración Git está habilitada.

#### git_integration
Instancia de la integración Git (si está disponible).

## Clase Entry

### Propiedades

- `entry_id` (str): ID único de la entrada
- `entry_type` (str): Tipo de entrada
- `title` (str): Título de la entrada
- `content` (str): Contenido de la entrada
- `tags` (List[str]): Lista de etiquetas
- `files_affected` (List[str]): Lista de archivos afectados
- `llm_context` (str): Contexto específico para LLM
- `related_entries` (List[str]): Lista de IDs de entradas relacionadas
- `created_at` (str): Fecha de creación (ISO format)
- `updated_at` (str): Fecha de última actualización (ISO format)
- `git_info` (Dict, opcional): Información de Git si está disponible

### Métodos

#### to_dict()
Convierte la entrada a diccionario.

```python
def to_dict(self) -> Dict[str, Any]
```

#### from_dict()
Crea una entrada desde un diccionario.

```python
@classmethod
def from_dict(cls, data: Dict[str, Any]) -> 'Entry'
```

## Manejo de Errores

### Errores Comunes

#### ValueError: "Tipo de entrada inválido"
**Causa**: El tipo de entrada no es uno de los válidos.
**Solución**: Usar solo: `'decision'`, `'change'`, `'context'`, `'bug'`, `'feature'`, `'note'`

```python
# ❌ INCORRECTO
m.create_entry('Configuración', 'Título', 'Contenido')

# ✅ CORRECTO
m.create_entry('note', 'Configuración', 'Título', 'Contenido')
```

#### AttributeError: El proyecto no está inicializado
**Causa**: No se llamó `initialize_project()` antes de usar otros métodos.
**Solución**: Siempre inicializar primero.

```python
# ❌ INCORRECTO
m = MemorySystem('proyecto')
m.create_entry('note', 'Título', 'Contenido')

# ✅ CORRECTO
m = MemorySystem('proyecto')
m.initialize_project()  # REQUERIDO
m.create_entry('note', 'Título', 'Contenido')
```

#### TypeError: Orden de parámetros incorrecto
**Causa**: Los parámetros están en el orden incorrecto.
**Solución**: Seguir el orden: `entry_type`, `title`, `content`, `tags`, ...

```python
# ❌ INCORRECTO - orden mal
m.create_entry('Título', 'Contenido', 'note', ['tags'])

# ✅ CORRECTO - orden correcto
m.create_entry('note', 'Título', 'Contenido', ['tags'])
```

### Patrón Recomendado para Manejo de Errores

```python
try:
    # Crear entrada
    entry_id = m.create_entry(
        'note',
        'Título de prueba',
        'Contenido de prueba',
        ['test']
    )
    print(f"Entrada creada con ID: {entry_id}")
    
except ValueError as e:
    print(f"Error de validación: {e}")
    print("Tipos válidos: decision, change, context, bug, feature, note")
    
except Exception as e:
    print(f"Error inesperado: {e}")
    # Verificar que el proyecto esté inicializado
    if not m.project_root.exists():
        print("El proyecto no está inicializado. Ejecuta initialize_project() primero.")
```

## Casos de Uso Comunes

### Para Agentes LLM

```python
# Antes de implementar cambios, revisar contexto
recent_context = m.list_entries(
    entry_type='context',
    limit=5
)

# Buscar decisiones relacionadas
related_decisions = m.list_entries(
    entry_type='decision',
    search='base de datos'
)

# Registrar nueva implementación
m.create_entry(
    'change',
    'Implementación basada en decisiones anteriores',
    'Se implementó siguiendo las decisiones de arquitectura documentadas.',
    ['implementacion'],
    related_entries=[d.entry_id for d in related_decisions]
)
```

### Para Scripts de Automatización

```python
# Script que registra automáticamente cambios
def record_deployment(deployment_info):
    m.create_entry(
        'change',
        f'Deployment {deployment_info["version"]}',
        f'Deployment automático completado. Cambios: {deployment_info["changes"]}',
        ['deployment', 'automatizacion'],
        llm_context='Información para debugging y auditoría de deployments automáticos'
    )

# Script que registra métricas
def record_metrics(metrics_data):
    m.create_entry(
        'note',
        'Métricas de rendimiento',
        f'CPU: {metrics_data["cpu"]}%, Memoria: {metrics_data["memory"]}%',
        ['metricas', 'rendimiento'],
        llm_context='Datos para análisis de tendencias de rendimiento'
    )
```

## Mejores Prácticas

1. **Siempre inicializar**: Llamar `initialize_project()` antes de usar otros métodos
2. **Manejar errores**: Usar try-catch para manejar errores de validación
3. **Validar parámetros**: Verificar que los tipos de entrada sean válidos
4. **Usar etiquetas consistentes**: Mantener un vocabulario de etiquetas coherente
5. **Proporcionar contexto LLM**: Usar el parámetro `llm_context` para información específica de IA
6. **Referenciar entradas**: Usar `related_entries` para crear trazabilidad
7. **Manejar archivos**: Especificar `files_affected` para cambios de código

## Ejemplos Completos

### Ejemplo 1: Configuración Inicial

```python
from memoria_cursor import MemorySystem

# Inicializar sistema
m = MemorySystem('mi-proyecto-web')
m.initialize_project()

# Registrar configuración
config_id = m.create_entry(
    'context',
    'Configuración del proyecto',
    'Proyecto web con Flask, PostgreSQL y Redis. Python 3.8+, PostgreSQL 12+, Redis 6+.',
    ['configuracion', 'flask', 'postgresql', 'redis']
)

print(f"Proyecto inicializado con ID: {config_id}")
```

### Ejemplo 2: Workflow Completo

```python
from memoria_cursor import MemorySystem

# Inicializar
m = MemorySystem('proyecto-api')
m.initialize_project()

# 1. Registrar decisión de arquitectura
decision_id = m.create_entry(
    'decision',
    'API REST con FastAPI',
    'Se eligió FastAPI por su rendimiento, validación automática y documentación automática.',
    ['arquitectura', 'api', 'fastapi']
)

# 2. Registrar implementación
impl_id = m.create_entry(
    'change',
    'Implementación de API base',
    'Se implementó estructura base de la API con FastAPI, incluyendo routers y middleware.',
    ['implementacion', 'api', 'fastapi'],
    files_affected=['main.py', 'api/', 'middleware.py'],
    related_entries=[decision_id]
)

# 3. Registrar bug encontrado
bug_id = m.create_entry(
    'bug',
    'Error en validación de parámetros',
    'Se encontró error en validación de parámetros opcionales en endpoints POST.',
    ['bug', 'validacion', 'fastapi'],
    files_affected=['api/endpoints.py'],
    related_entries=[impl_id]
)

# 4. Registrar solución
solution_id = m.create_entry(
    'change',
    'Corrección de validación de parámetros',
    'Se corrigió el error de validación implementando validadores personalizados.',
    ['correccion', 'validacion', 'fastapi'],
    files_affected=['api/endpoints.py', 'validators.py'],
    related_entries=[bug_id]
)

# 5. Exportar para revisión
m.export_entries(format='markdown')
print("Workflow completado y memoria exportada")
```

## Integración con Herramientas Externas

### Git Hooks

```python
# pre-commit hook
def document_changes():
    modified_files = get_git_modified_files()  # Función externa
    
    if modified_files:
        m.create_entry(
            'change',
            'Cambios antes del commit',
            f'Archivos modificados: {", ".join(modified_files)}',
            ['commit', 'git'],
            files_affected=modified_files
        )

# Ejecutar antes del commit
document_changes()
```

### CI/CD Pipelines

```python
# Pipeline de deployment
def record_deployment_pipeline():
    m.create_entry(
        'change',
        'Pipeline de CI/CD ejecutado',
        'Pipeline completado exitosamente. Tests pasaron, build generado, deployment iniciado.',
        ['ci-cd', 'deployment', 'pipeline'],
        llm_context='Información para debugging de pipelines y auditoría de deployments'
    )
```

Esta documentación proporciona una guía completa para usar la API Python del módulo `memoria-cursor`, incluyendo todos los métodos disponibles, manejo de errores, mejores prácticas y ejemplos prácticos.
