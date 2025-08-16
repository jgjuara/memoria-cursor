# Guía para Agentes LLM - Sistema de Memoria

## 🎯 Propósito de este Documento

Esta guía está diseñada específicamente para agentes LLM (como Cursor AI, Claude, etc.) que necesiten usar el módulo `memoria-cursor` para documentar cambios y decisiones en proyectos de desarrollo.

## 🚀 Inicio Rápido (3 Pasos)

### 1. Importar e Inicializar
```python
from memoria_cursor import MemorySystem

# Crear instancia del sistema
m = MemorySystem('nombre-del-proyecto')

# IMPORTANTE: Siempre inicializar primero
m.initialize_project()
```

### 2. Crear una Entrada
```python
# Formato: m.create_entry(tipo, título, contenido, etiquetas)
entry_id = m.create_entry(
    'note',  # tipo de entrada
    'Título descriptivo',  # título
    'Contenido detallado de la entrada',  # contenido
    ['etiqueta1', 'etiqueta2']  # etiquetas (opcional)
)
```

### 3. Verificar que Funcionó
```python
print(f"Entrada creada con ID: {entry_id}")
```

## 📋 Tipos de Entrada Válidos

**Solo estos 6 tipos son válidos:**
- `'decision'` - Decisiones de arquitectura y diseño
- `'change'` - Cambios importantes en el código
- `'context'` - Información de contexto del proyecto
- `'bug'` - Problemas y bugs encontrados
- `'feature'` - Nuevas funcionalidades implementadas
- `'note'` - Notas generales y observaciones

## ⚠️ Errores Comunes y Soluciones

### Error 1: "Tipo de entrada inválido"
**Causa**: Usaste un tipo que no está en la lista de arriba
**Solución**: Usa solo uno de los 6 tipos válidos

```python
# ❌ INCORRECTO
m.create_entry('Configuración', 'Título', 'Contenido')

# ✅ CORRECTO
m.create_entry('note', 'Configuración', 'Título', 'Contenido')
```

### Error 2: "El proyecto no está inicializado"
**Causa**: No llamaste `initialize_project()` antes de crear entradas
**Solución**: Siempre inicializar primero

```python
# ❌ INCORRECTO
m = MemorySystem('proyecto')
m.create_entry('note', 'Título', 'Contenido')

# ✅ CORRECTO
m = MemorySystem('proyecto')
m.initialize_project()  # REQUERIDO
m.create_entry('note', 'Título', 'Contenido')
```

### Error 3: "Orden de parámetros incorrecto"
**Causa**: Los parámetros están en el orden incorrecto
**Solución**: Usar este orden exacto: `tipo`, `título`, `contenido`, `etiquetas`

```python
# ❌ INCORRECTO - orden mal
m.create_entry('Título', 'Contenido', 'note', ['tags'])

# ✅ CORRECTO - orden correcto
m.create_entry('note', 'Título', 'Contenido', ['tags'])
```

## 🔧 Métodos Principales

### Crear Entrada
```python
m.create_entry(
    tipo_entrada,      # str: uno de los 6 tipos válidos
    titulo,            # str: título descriptivo
    contenido,         # str: contenido detallado
    etiquetas=None,    # List[str]: etiquetas opcionales
    archivos=None,     # List[str]: archivos afectados opcionales
    contexto_llm=None, # str: contexto específico para LLM opcional
    entradas_rel=None  # List[str]: IDs de entradas relacionadas opcional
)
```

### Listar Entradas
```python
# Obtener todas las entradas
entradas = m.list_entries()

# Filtrar por tipo
decisiones = m.list_entries(entry_type='decision')

# Buscar por texto
resultados = m.list_entries(search='postgresql')

# Limitar cantidad
recientes = m.list_entries(limit=5)
```

### Obtener Entrada Específica
```python
entrada = m.get_entry('id-de-la-entrada')
if entrada:
    print(f"Título: {entrada.title}")
    print(f"Tipo: {entrada.entry_type}")
```

## 📝 Ejemplos Prácticos para LLMs

### Ejemplo 1: Documentar una Decisión
```python
from memoria_cursor import MemorySystem

m = MemorySystem('mi-proyecto')
m.initialize_project()

decision_id = m.create_entry(
    'decision',
    'Elección de base de datos PostgreSQL',
    'Se eligió PostgreSQL por su robustez ACID, soporte JSON nativo y excelente rendimiento para consultas complejas. Alternativas consideradas: MongoDB (menos consistencia), MySQL (limitaciones JSON), SQLite (concurrencia limitada).',
    ['arquitectura', 'base-datos', 'postgresql'],
    files_affected=['config/database.py', 'models/'],
    llm_context='Decisión fundamental que afecta toda la arquitectura de persistencia del sistema'
)

print(f"Decisión documentada con ID: {decision_id}")
```

### Ejemplo 2: Documentar un Cambio en el Código
```python
# Después de implementar cambios
cambio_id = m.create_entry(
    'change',
    'Implementación de autenticación JWT',
    'Se implementó sistema de autenticación basado en JWT tokens. Incluye: login/logout, validación de tokens, middleware de autenticación. Basado en la decisión anterior de usar PostgreSQL.',
    ['implementacion', 'autenticacion', 'jwt', 'seguridad'],
    files_affected=['auth.py', 'middleware.py', 'models.py'],
    related_entries=[decision_id]  # Referenciar decisión anterior
)

print(f"Cambio documentado con ID: {cambio_id}")
```

### Ejemplo 3: Documentar un Bug Encontrado
```python
bug_id = m.create_entry(
    'bug',
    'Error en validación de parámetros opcionales',
    'Se encontró error en validación de parámetros opcionales en endpoints POST. Los parámetros con valores por defecto no se validaban correctamente, causando errores 500.',
    ['bug', 'validacion', 'api'],
    files_affected=['api/endpoints.py'],
    llm_context='Problema crítico que afecta la estabilidad de la API'
)

print(f"Bug documentado con ID: {bug_id}")
```

### Ejemplo 4: Documentar Contexto del Proyecto
```python
contexto_id = m.create_entry(
    'context',
    'Configuración del entorno de desarrollo',
    'El proyecto requiere Python 3.8+, PostgreSQL 12+, Redis 6+. Variables de entorno críticas: DATABASE_URL, REDIS_URL, SECRET_KEY. Para desarrollo local: docker-compose up -d postgres redis.',
    ['configuracion', 'entorno', 'dependencias'],
    files_affected=['requirements.txt', '.env.example', 'docker-compose.yml'],
    llm_context='Información esencial para setup y desarrollo del proyecto'
)

print(f"Contexto documentado con ID: {contexto_id}")
```

## 🔍 Patrones de Uso Recomendados

### Antes de Implementar Cambios
```python
# 1. Revisar contexto reciente
contexto_reciente = m.list_entries(entry_type='context', limit=3)

# 2. Buscar decisiones relacionadas
decisiones_relacionadas = m.list_entries(
    entry_type='decision', 
    search='palabra_clave'
)

# 3. Verificar archivos afectados
cambios_previos = m.list_entries(
    files_affected=['archivo_a_modificar.py']
)
```

### Después de Implementar Cambios
```python
# 1. Documentar el cambio
cambio_id = m.create_entry(
    'change',
    'Descripción del cambio implementado',
    'Detalles de lo que se implementó y por qué',
    ['implementacion', 'categoria'],
    files_affected=['archivos_modificados.py'],
    related_entries=[decisiones_relacionadas[0].entry_id]  # Si hay decisión relacionada
)

# 2. Exportar para revisión
m.export_entries()
```

## 📊 Casos de Uso Específicos para LLMs

### Para Refactoring de Código
```python
# Antes del refactoring
refactor_id = m.create_entry(
    'change',
    'Refactoring del módulo de autenticación',
    'Se refactorizó el módulo de autenticación para mejorar la separación de responsabilidades. Cambios: extracción de lógica de negocio a servicios, simplificación de controladores, mejora de testabilidad.',
    ['refactoring', 'autenticacion', 'arquitectura'],
    files_affected=['auth/', 'services/', 'controllers/'],
    llm_context='Refactoring que mejora la arquitectura y mantenibilidad del código'
)
```

### Para Migración de Dependencias
```python
migracion_id = m.create_entry(
    'change',
    'Migración de Django 3.2 a 4.2',
    'Se migró Django de versión 3.2 a 4.2. Cambios: actualización de sintaxis, nuevas características de seguridad, mejoras de rendimiento. Breaking changes documentados y resueltos.',
    ['migracion', 'django', 'dependencias'],
    files_affected=['requirements.txt', 'settings.py', 'urls.py'],
    llm_context='Migración mayor que requiere atención especial a breaking changes'
)
```

### Para Documentar Lecciones Aprendidas
```python
leccion_id = m.create_entry(
    'note',
    'Lección aprendida: Cache de Redis en producción',
    'Se aprendió que el cache de Redis debe configurarse con TTL apropiado en producción. Sin TTL, la memoria se llena y causa problemas de rendimiento. Implementar limpieza automática y monitoreo de memoria.',
    ['leccion', 'redis', 'cache', 'produccion'],
    files_affected=['config/cache.py', 'monitoring/'],
    llm_context='Lección importante para evitar problemas futuros en producción'
)
```

## 🚨 Checklist para LLMs

Antes de usar el módulo, verifica:

- [ ] ¿Importaste `MemorySystem` correctamente?
- [ ] ¿Llamaste `initialize_project()` después de crear la instancia?
- [ ] ¿Usaste uno de los 6 tipos de entrada válidos?
- [ ] ¿Los parámetros están en el orden correcto?
- [ ] ¿Manejas posibles errores con try-catch?

## 🔧 Comando de Prueba

Para verificar que todo funciona:

```python
from memoria_cursor import MemorySystem

try:
    m = MemorySystem('test-proyecto')
    m.initialize_project()
    
    test_id = m.create_entry(
        'note',
        'Prueba de funcionamiento',
        'Esta es una entrada de prueba para verificar que el sistema funciona correctamente.',
        ['test', 'verificacion']
    )
    
    print(f"✅ Sistema funcionando correctamente. Entrada creada: {test_id}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Verifica la instalación y configuración del módulo")
```

## 📚 Recursos Adicionales

- **Documentación completa**: Ver `docs/api-python.md`
- **Ejemplos avanzados**: Ver `docs/ejemplos.md`
- **Guía de uso general**: Ver `docs/guia-uso.md`

## 🎯 Resumen para LLMs

**Recuerda siempre:**
1. **Importar**: `from memoria_cursor import MemorySystem`
2. **Inicializar**: `m.initialize_project()` (REQUERIDO)
3. **Crear**: `m.create_entry(tipo, título, contenido, etiquetas)`
4. **Tipos válidos**: Solo `decision`, `change`, `context`, `bug`, `feature`, `note`
5. **Orden de parámetros**: `tipo` primero, luego `título`, `contenido`, `etiquetas`

Siguiendo esta guía, podrás usar el módulo `memoria-cursor` correctamente sin los errores comunes que experimentan otros agentes LLM.
