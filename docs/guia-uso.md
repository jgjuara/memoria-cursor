# Guía de Uso - Sistema de Memoria para Agentes LLM

## Descripción General

El Sistema de Memoria es una herramienta diseñada para registrar información relevante del desarrollo de proyectos que puede alimentar las interacciones con agentes LLM (Cursor, Claude Code, etc.). Proporciona una estructura organizada para documentar decisiones, cambios, contexto y observaciones del proyecto.

## Instalación en un Nuevo Proyecto

### Requisitos Previos
- Python 3.7+
- Git (opcional, para integración automática)

### Proceso de Instalación

1. **Instalar el módulo**:
   ```bash
   # Opción 1: Desde PyPI (cuando esté disponible)
   pip install memoria-cursor
   
   # Opción 2: Desde git usando uv (más rápido)
   uv pip install git+https://github.com/tu-usuario/memoria-cursor.git
   
   # Opción 3: Desde fuente
   git clone https://github.com/tu-usuario/memoria-cursor.git
   cd memoria-cursor
   pip install -e .
   ```

2. **Inicializar en tu proyecto**:
   ```bash
   cd /path/to/tu-proyecto
   memoria init --name "Nombre del Proyecto" --description "Descripción del proyecto"
   ```

3. **Verificar la instalación**:
   ```bash
   memoria create note "Instalación completada" "Sistema de memoria instalado exitosamente"
   memoria list
   ```

## Estructura del Sistema

```
tu-proyecto/
├── config/                # Configuración del sistema
│   ├── schema.json        # Esquema de validación
│   └── config.json        # Configuración del proyecto
├── entries/               # Entradas de memoria del proyecto
│   └── entries.json
├── export/                # Exportaciones para LLM
├── MEMORIA.md             # Documentación del proyecto
└── .gitignore             # Configurado automáticamente
```

## Uso Básico

### Crear una Entrada

```bash
memoria create <tipo> "<titulo>" "<contenido>" [opciones]
```

**Tipos de entrada disponibles**:
- `decision` - Decisiones de arquitectura y diseño
- `change` - Cambios importantes en el código
- `context` - Información de contexto del proyecto
- `bug` - Problemas y bugs encontrados
- `feature` - Nuevas funcionalidades implementadas
- `note` - Notas generales y observaciones

**Ejemplos**:
```bash
# Registrar una decisión
memoria create decision "Elección de base de datos" "Se eligió PostgreSQL por su robustez y soporte JSON nativo" --tags "arquitectura" "base-datos"

# Registrar un cambio
memoria create change "Implementación de autenticación" "Se agregó sistema JWT para autenticación de usuarios" --files "auth.py" "models.py" --tags "autenticacion"

# Registrar contexto
memoria create context "Configuración del entorno" "El proyecto requiere Python 3.8+ y PostgreSQL 12+" --tags "configuracion"

# Registrar entrada relacionada con decisiones anteriores
memoria create change "Implementación de autenticación" "Se implementó sistema JWT basado en la decisión de arquitectura anterior" --related-entries "550e8400-e29b-41d4-a716-446655440000" "6ba7b810-9dad-11d1-80b4-00c04fd430c8" --tags "implementacion" "autenticacion"
```

### Opciones Adicionales

- `--tags` - Etiquetas para categorizar la entrada
- `--files` - Archivos afectados por el cambio
- `--llm-context` - Información específica para agentes LLM
- `--related-entries` - IDs de entradas relacionadas para contexto y trazabilidad

### Listar Entradas

```bash
# Listar todas las entradas
memoria list

# Listar últimas 10 entradas
memoria list --limit 10

# Filtrar por tipo
memoria list --type decision

# Buscar por contenido
memoria list --search "postgresql"

# Filtrar por etiquetas
memoria list --tags "arquitectura" "base-datos"

# Ver estadísticas
memoria list --stats
```

### Exportar para LLM

```bash
# Exportar en formato Markdown (por defecto)
memoria export

# Exportar en formato JSON
memoria export --format json

# Exportar en formato texto
memoria export --format text

# Excluir información de Git
memoria export --no-git

# Agrupar por fecha en lugar de tipo
memoria export --group-by date

# Limitar número de entradas
memoria export --limit 50
```

## Entradas Relacionadas

El sistema permite referenciar otras entradas para crear un contexto más rico y trazable:

### Cuándo Usar Entradas Relacionadas

- **Decisiones consecutivas**: Cuando una decisión se basa en otra anterior
- **Cambios relacionados**: Cuando un cambio implementa o modifica algo documentado previamente
- **Bugs y soluciones**: Conectar el reporte del bug con su resolución
- **Contexto histórico**: Referenciar decisiones de arquitectura que afectan implementaciones actuales

### Ejemplo de Uso

```bash
# Primera entrada: Decisión de arquitectura
memoria create decision "Elección de base de datos" "Se eligió PostgreSQL por su robustez ACID" --tags "arquitectura" "base-datos"

# Segunda entrada: Referenciando la decisión anterior
memoria create change "Configuración de PostgreSQL" "Se configuró la base de datos según la decisión de arquitectura" --related-entries "550e8400-e29b-41d4-a716-446655440000" --tags "implementacion" "configuracion"
```

### Beneficios

- **Trazabilidad**: Seguir el hilo de decisiones y cambios
- **Contexto**: Entender mejor una entrada viendo sus referencias
- **Navegación**: Explorar el historial del proyecto de manera inteligente
- **Análisis**: Identificar patrones y dependencias entre cambios

## Integración con Git

El sistema captura automáticamente información de Git cuando está disponible:

- **Commit actual**: Hash del commit en el que se registra la entrada
- **Rama**: Rama de trabajo actual
- **Estado**: Si el repositorio está limpio o con cambios pendientes
- **Mensaje**: Mensaje del commit actual

Esta información se incluye automáticamente en cada entrada y se puede ver con:
```bash
memoria list --show-git
```

## Configuración

### Archivo de Configuración

El archivo `config/config.json` contiene la configuración del sistema:

```json
{
  "project": {
    "name": "Nombre del Proyecto",
    "description": "Descripción del proyecto",
    "version": "1.0.1"
  },
  "system": {
    "auto_git": true,
    "default_entry_type": "note",
    "max_content_length": 10000,
    "backup_enabled": true
  },
  "export": {
    "default_format": "markdown",
    "include_git_info": true,
    "group_by": "type"
  }
}
```

### Personalización

Puedes modificar la configuración editando el archivo `config.json` en el directorio `config/`.

## Mejores Prácticas

### Cuándo Registrar Información

**Siempre registrar cuando**:
- Se toman decisiones de arquitectura o diseño
- Se implementan cambios significativos en el código
- Se resuelven bugs o problemas importantes
- Se agregan nuevas funcionalidades
- Se cambia la configuración del proyecto
- Se documenta contexto relevante para futuras interacciones

### Cómo Escribir Entradas Efectivas

1. **Ser específico**: Incluir detalles técnicos relevantes
2. **Usar etiquetas**: Facilitar búsquedas futuras
3. **Referenciar archivos**: Conectar entradas con código específico
4. **Incluir contexto**: Explicar el "por qué" además del "qué"
5. **Mantener consistencia**: Usar el mismo formato y estructura
6. **Actualizar regularmente**: Registrar información mientras está fresca

### Estructura Recomendada para Entradas

```
Título: Descriptivo y específico
Contenido:
- Contexto: ¿Por qué se tomó esta decisión?
- Alternativas: ¿Qué otras opciones se consideraron?
- Implementación: ¿Cómo se implementó?
- Impacto: ¿Qué efectos tiene en el proyecto?
- Archivos: ¿Qué archivos están involucrados?
```

## Comandos de Conveniencia

### Alias Recomendados

Agregar a tu `.bashrc` o `.zshrc`:

```bash
alias memoria-create='memoria create'
alias memoria-list='memoria list'
alias memoria-export='memoria export'
alias memoria-stats='memoria list --stats'
```

### Scripts de Conveniencia

Crear scripts específicos del proyecto para casos de uso comunes:

```bash
# scripts/record-decision.sh
#!/bin/bash
memoria create decision "$1" "$2" --tags "${3:-decision}"

# scripts/record-change.sh
#!/bin/bash
memoria create change "$1" "$2" --files "$3" --tags "${4:-change}"
```

## Solución de Problemas

### Problemas Comunes

1. **Error: "Script debe ejecutarse desde el directorio raíz"**
   - Solución: Asegúrate de estar en el directorio raíz del proyecto

2. **Error: "No se pudo obtener información de Git"**
   - Solución: El proyecto no es un repositorio Git o Git no está instalado
   - El sistema funciona sin Git, solo no capturará información de commits

3. **Error: "Tipo de entrada inválido"**
   - Solución: Usar uno de los tipos válidos: decision, change, context, bug, feature, note

4. **Archivo entries.json corrupto**
   - Solución: Hacer backup y regenerar el archivo desde cero

### Logs y Debugging

Para obtener más información sobre errores:
```bash
memoria create --help
memoria list --help
memoria export --help
```

## Migración desde bitacora.md

Si tienes un archivo `bitacora.md` existente:

1. **Exportar contenido**: Convertir entradas importantes a formato JSON
2. **Instalar sistema**: Usar el script de instalación
3. **Migrar entradas**: Crear entradas usando las herramientas del sistema
4. **Verificar**: Listar entradas para confirmar la migración

## Mantenimiento

### Actualizaciones

Para actualizar el sistema en un proyecto:

1. Descargar la nueva versión de memoria-cursor
2. Ejecutar el script de instalación nuevamente
3. Los archivos de configuración se preservarán

### Backup

El sistema incluye backup automático configurado en `config.json`. Los archivos de backup se guardan en el directorio `entries/`.

### Limpieza

Para limpiar entradas antiguas o duplicadas:

```bash
# Ver estadísticas antes de limpiar
memoria list --stats

# Exportar antes de limpiar
memoria export --format json
```

## Integración con Agentes LLM

### Para Agentes LLM

Los agentes LLM deben:

1. **Revisar entradas recientes** antes de implementar cambios: `memoria list --limit 5`
2. **Registrar decisiones** importantes durante el desarrollo: `memoria create decision`
3. **Documentar cambios** significativos en el código: `memoria create change`
4. **Usar etiquetas** para facilitar búsquedas futuras
5. **Exportar memoria** cuando sea necesario compartir contexto

### Comandos para Agentes

```bash
# Antes de implementar cambios
memoria list --limit 5
memoria list --type decision --search "palabra-clave"

# Después de implementar cambios
memoria create change "Descripción" "Detalles" --files "archivo1.py" "archivo2.py"

# Para decisiones importantes
memoria create decision "Título" "Justificación" --tags "categoria1" "categoria2"
```

## Recursos Adicionales

- **Reglas detalladas**: Ver `docs/reglas-agentes-llm.md`
- **Documentación del proyecto**: Ver `docs/guia-uso.md`
- **Ejemplos**: Ver `docs/ejemplos.md`
- **Esquema JSON**: Ver `memoria_cursor/config/schema.json`

## Soporte

Para reportar problemas o solicitar mejoras:
- Crear un issue en el repositorio de memoria-cursor
- Incluir información del sistema y pasos para reproducir
- Adjuntar archivos de configuración relevantes

## Uso Programático (API Python)

### Importación e Inicialización

Para usar el módulo desde código Python, primero debes importar la clase principal:

```python
from memoria_cursor import MemorySystem
```

Luego crear una instancia del sistema y inicializarlo:

```python
# Crear instancia del sistema
m = MemorySystem('nombre-proyecto')

# Inicializar el proyecto (REQUERIDO antes de usar cualquier método)
m.initialize_project()
```

**Nota importante**: Siempre debes llamar `initialize_project()` antes de usar otros métodos. Este método:
- Crea la estructura de directorios necesaria
- Inicializa archivos de configuración
- Configura la integración con Git si está disponible

### Crear Entradas Programáticamente

El método principal para crear entradas es `create_entry()`. Su firma es:

```python
def create_entry(
    self,
    entry_type: str,           # Tipo de entrada (requerido)
    title: str,                # Título descriptivo (requerido)
    content: str,              # Contenido principal (requerido)
    tags: Optional[List[str]] = None,           # Etiquetas opcionales
    files_affected: Optional[List[str]] = None, # Archivos afectados opcionales
    llm_context: Optional[str] = None,          # Contexto para LLM opcional
    related_entries: Optional[List[str]] = None # Entradas relacionadas opcionales
) -> str
```

**Ejemplos de uso**:

```python
# Crear una nota simple
entry_id = m.create_entry(
    'note',
    'Configuración inicial del proyecto',
    'Se instaló memoria-cursor y se creó la documentación base del proyecto.',
    ['configuracion', 'memoria-cursor', 'documentacion']
)

# Crear una decisión con contexto completo
decision_id = m.create_entry(
    'decision',
    'Elección de base de datos',
    'Se eligió PostgreSQL por su robustez ACID, soporte JSON nativo y excelente rendimiento.',
    ['arquitectura', 'base-datos', 'postgresql'],
    files_affected=['config/database.py', 'models/', 'migrations/'],
    llm_context='Decisión de arquitectura que afecta toda la capa de persistencia del sistema',
    related_entries=[entry_id]  # Referenciar entrada anterior
)

# Crear un cambio con archivos afectados
change_id = m.create_entry(
    'change',
    'Implementación de autenticación JWT',
    'Se implementó sistema de autenticación basado en JWT tokens.',
    ['implementacion', 'autenticacion', 'jwt'],
    files_affected=['auth.py', 'middleware.py', 'models.py'],
    llm_context='Cambio que afecta la seguridad y autenticación de usuarios'
)
```

### Consultar y Filtrar Entradas

#### Listar Entradas

```python
# Obtener todas las entradas
all_entries = m.list_entries()

# Filtrar por tipo
decisions = m.list_entries(entry_type='decision')
changes = m.list_entries(entry_type='change')
notes = m.list_entries(entry_type='note')

# Limitar número de resultados
recent_entries = m.list_entries(limit=10)

# Filtrar por etiquetas
config_entries = m.list_entries(tags=['configuracion'])
arch_entries = m.list_entries(tags=['arquitectura'])
```

#### Búsqueda Avanzada

```python
# Buscar por texto en título y contenido
search_results = m.list_entries(search='postgresql')

# Filtrar por rango de fechas
from datetime import datetime, timedelta
yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
recent_entries = m.list_entries(date_from=yesterday)

# Combinar filtros
recent_decisions = m.list_entries(
    entry_type='decision',
    limit=5,
    tags=['arquitectura']
)
```

#### Obtener Entrada Específica

```python
# Obtener entrada por ID
entry = m.get_entry(entry_id)

if entry:
    print(f"Título: {entry.title}")
    print(f"Tipo: {entry.entry_type}")
    print(f"Contenido: {entry.content}")
    print(f"Etiquetas: {entry.tags}")
    print(f"Fecha: {entry.created_at}")
```

### Exportar para LLM

```python
# Exportar en formato Markdown (por defecto)
m.export_entries()

# Exportar en formato JSON
m.export_entries(format='json')

# Exportar solo entradas de un tipo específico
decisions = m.list_entries(entry_type='decision')
# Luego procesar manualmente o usar herramientas de exportación
```

### Gestión de Entradas

```python
# Actualizar una entrada existente
m.update_entry(
    entry_id,
    title='Título actualizado',
    content='Contenido actualizado',
    tags=['nueva', 'etiqueta']
)

# Eliminar una entrada
m.delete_entry(entry_id)

# Obtener estadísticas del sistema
stats = m.get_statistics()
print(f"Total de entradas: {stats['total_entries']}")
print(f"Última actualización: {stats['last_updated']}")
```

### Manejo de Errores

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
    # Verificar tipos de entrada válidos
    print("Tipos válidos: decision, change, context, bug, feature, note")
    
except Exception as e:
    print(f"Error inesperado: {e}")
    # Verificar que el proyecto esté inicializado
    if not m.project_root.exists():
        print("El proyecto no está inicializado. Ejecuta initialize_project() primero.")
```

### Casos de Uso Comunes

#### Para Agentes LLM

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

#### Para Scripts de Automatización

```python
# Script que registra automáticamente cambios
def record_deployment(deployment_info):
    m.create_entry(
        'change',
        f'Deployment {deployment_info["version"]}',
        f'Deployment automático completado. Cambios: {deployment_info["changes"]}',
        ['deployment', 'automatizacion'],
        llm_context='Información para debugging y auditoría de deployments'
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

### Mejores Prácticas para Uso Programático

1. **Siempre inicializar**: Llamar `initialize_project()` antes de usar otros métodos
2. **Manejar errores**: Usar try-catch para manejar errores de validación
3. **Validar parámetros**: Verificar que los tipos de entrada sean válidos
4. **Usar etiquetas consistentes**: Mantener un vocabulario de etiquetas coherente
5. **Proporcionar contexto LLM**: Usar el parámetro `llm_context` para información específica de IA
6. **Referenciar entradas**: Usar `related_entries` para crear trazabilidad
7. **Manejar archivos**: Especificar `files_affected` para cambios de código

### Solución de Problemas Comunes

#### Error: "Tipo de entrada inválido"
```python
# ❌ INCORRECTO
m.create_entry('Configuración', 'Título', 'Contenido')

# ✅ CORRECTO
m.create_entry('note', 'Configuración', 'Título', 'Contenido')
```

#### Error: "El proyecto no está inicializado"
```python
# ❌ INCORRECTO
m = MemorySystem('proyecto')
m.create_entry('note', 'Título', 'Contenido')

# ✅ CORRECTO
m = MemorySystem('proyecto')
m.initialize_project()  # REQUERIDO
m.create_entry('note', 'Título', 'Contenido')
```

#### Error: "Orden de parámetros incorrecto"
```python
# ❌ INCORRECTO - orden mal
m.create_entry('Título', 'Contenido', 'note', ['tags'])

# ✅ CORRECTO - orden correcto
m.create_entry('note', 'Título', 'Contenido', ['tags'])
```
