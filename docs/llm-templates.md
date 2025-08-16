# Plantillas para Agentes LLM - Sistema de Memoria

## 🎯 Propósito

Este archivo contiene plantillas de código listas para usar que los agentes LLM pueden copiar y adaptar para diferentes situaciones.

## 📋 Plantilla Básica de Inicialización

```python
from memoria_cursor import MemorySystem

# Inicializar sistema de memoria
m = MemorySystem('nombre-del-proyecto')
m.initialize_project()

print("✅ Sistema de memoria inicializado correctamente")
```

## 🏗️ Plantillas por Tipo de Entrada

### 1. Plantilla para Decisiones de Arquitectura

```python
# Plantilla para documentar decisiones de arquitectura
decision_id = m.create_entry(
    'decision',
    'TÍTULO_DE_LA_DECISIÓN',
    '''DESCRIPCIÓN_DETALLADA:
- ¿Qué se decidió?
- ¿Por qué se tomó esta decisión?
- ¿Qué alternativas se consideraron?
- ¿Cuál es el impacto en el proyecto?''',
    ['arquitectura', 'CATEGORIA_ESPECIFICA'],
    files_affected=['archivos/afectados.py'],
    llm_context='CONTEXTO_ESPECIFICO_PARA_AGENTES_LLM'
)

print(f"Decisión documentada con ID: {decision_id}")
```

### 2. Plantilla para Cambios en el Código

```python
# Plantilla para documentar cambios implementados
cambio_id = m.create_entry(
    'change',
    'DESCRIPCIÓN_DEL_CAMBIO',
    '''DETALLES_DEL_CAMBIO:
- ¿Qué se implementó?
- ¿Cómo se implementó?
- ¿Por qué se hizo este cambio?
- ¿Cuáles son los beneficios?''',
    ['implementacion', 'CATEGORIA_ESPECIFICA'],
    files_affected=['archivos/modificados.py'],
    related_entries=[decision_id] if 'decision_id' in locals() else None,
    llm_context='CONTEXTO_PARA_AGENTES_LLM_FUTUROS'
)

print(f"Cambio documentado con ID: {cambio_id}")
```

### 3. Plantilla para Bugs Encontrados

```python
# Plantilla para documentar bugs
bug_id = m.create_entry(
    'bug',
    'DESCRIPCIÓN_DEL_BUG',
    '''DETALLES_DEL_BUG:
- ¿Cuál es el problema?
- ¿Cuáles son los síntomas?
- ¿En qué condiciones ocurre?
- ¿Cuál es el impacto?''',
    ['bug', 'CATEGORIA_ESPECIFICA'],
    files_affected=['archivos/afectados.py'],
    llm_context='INFORMACIÓN_CRÍTICA_PARA_DEBUGGING'
)

print(f"Bug documentado con ID: {bug_id}")
```

### 4. Plantilla para Contexto del Proyecto

```python
# Plantilla para documentar contexto
contexto_id = m.create_entry(
    'context',
    'TÍTULO_DEL_CONTEXTO',
    '''INFORMACIÓN_DE_CONTEXTO:
- ¿Cuál es el estado actual del proyecto?
- ¿Qué tecnologías se están usando?
- ¿Cuáles son los requisitos del entorno?
- ¿Qué información es crítica para nuevos desarrolladores?''',
    ['contexto', 'CATEGORIA_ESPECIFICA'],
    files_affected=['archivos/de/configuracion.py'],
    llm_context='INFORMACIÓN_ESENCIAL_PARA_ENTENDER_EL_PROYECTO'
)

print(f"Contexto documentado con ID: {contexto_id}")
```

### 5. Plantilla para Nuevas Funcionalidades

```python
# Plantilla para documentar nuevas funcionalidades
feature_id = m.create_entry(
    'feature',
    'NOMBRE_DE_LA_FUNCIONALIDAD',
    '''DETALLES_DE_LA_FUNCIONALIDAD:
- ¿Qué hace esta funcionalidad?
- ¿Cómo se implementó?
- ¿Qué tecnologías se usaron?
- ¿Cuáles son las características principales?''',
    ['feature', 'CATEGORIA_ESPECIFICA'],
    files_affected=['archivos/implementados.py'],
    related_entries=[decision_id] if 'decision_id' in locals() else None,
    llm_context='INFORMACIÓN_PARA_ENTENDER_LA_NUEVA_FUNCIONALIDAD'
)

print(f"Funcionalidad documentada con ID: {feature_id}")
```

### 6. Plantilla para Notas Generales

```python
# Plantilla para notas generales
nota_id = m.create_entry(
    'note',
    'TÍTULO_DE_LA_NOTA',
    '''CONTENIDO_DE_LA_NOTA:
- ¿Qué observación o nota quieres registrar?
- ¿Por qué es importante?
- ¿Qué información adicional es relevante?
- ¿Cuándo se aplica esta nota?''',
    ['nota', 'CATEGORIA_ESPECIFICA'],
    files_affected=['archivos/relevantes.py'] if 'archivos' else None,
    llm_context='INFORMACIÓN_GENERAL_PARA_AGENTES_LLM'
)

print(f"Nota documentada con ID: {nota_id}")
```

## 🔍 Plantillas para Consultas y Búsquedas

### Plantilla para Revisar Contexto Antes de Cambios

```python
# Plantilla para revisar contexto antes de implementar cambios
def revisar_contexto_antes_de_cambios():
    # 1. Obtener contexto reciente
    contexto_reciente = m.list_entries(
        entry_type='context',
        limit=5
    )
    
    # 2. Buscar decisiones relacionadas
    decisiones_relacionadas = m.list_entries(
        entry_type='decision',
        search='PALABRA_CLAVE_RELEVANTE'
    )
    
    # 3. Verificar archivos que se van a modificar
    cambios_previos = m.list_entries(
        files_affected=['archivo_a_modificar.py']
    )
    
    print(f"Contexto encontrado: {len(contexto_reciente)} entradas")
    print(f"Decisiones relacionadas: {len(decisiones_relacionadas)} entradas")
    print(f"Cambios previos en archivo: {len(cambios_previos)} entradas")
    
    return contexto_reciente, decisiones_relacionadas, cambios_previos

# Usar la función
contexto, decisiones, cambios = revisar_contexto_antes_de_cambios()
```

### Plantilla para Buscar Información Específica

```python
# Plantilla para buscar información específica
def buscar_informacion(palabra_clave, tipo_entrada=None, limite=10):
    resultados = m.list_entries(
        search=palabra_clave,
        entry_type=tipo_entrada,
        limit=limite
    )
    
    print(f"Resultados para '{palabra_clave}': {len(resultados)} entradas")
    
    for entrada in resultados:
        print(f"- [{entrada.entry_type.upper()}] {entrada.title}")
        if entrada.llm_context:
            print(f"  Contexto LLM: {entrada.llm_context}")
    
    return resultados

# Ejemplos de uso
decisiones_db = buscar_informacion('base de datos', 'decision')
cambios_auth = buscar_informacion('autenticación', 'change')
todo_postgres = buscar_informacion('postgresql')
```

## 📊 Plantillas para Workflows Completos

### Plantilla para Workflow de Implementación

```python
# Plantilla para workflow completo de implementación
def workflow_implementacion(titulo, descripcion, archivos, etiquetas, decision_relacionada=None):
    try:
        # 1. Crear entrada de cambio
        cambio_id = m.create_entry(
            'change',
            titulo,
            descripcion,
            etiquetas,
            files_affected=archivos,
            related_entries=[decision_relacionada] if decision_relacionada else None,
            llm_context='Implementación documentada para trazabilidad futura'
        )
        
        print(f"✅ Cambio implementado y documentado: {cambio_id}")
        
        # 2. Exportar para revisión
        m.export_entries()
        print("✅ Memoria exportada para revisión")
        
        return cambio_id
        
    except Exception as e:
        print(f"❌ Error al documentar implementación: {e}")
        return None

# Ejemplo de uso
cambio_id = workflow_implementacion(
    titulo="Implementación de autenticación JWT",
    descripcion="Se implementó sistema de autenticación basado en JWT tokens...",
    archivos=["auth.py", "middleware.py"],
    etiquetas=["implementacion", "autenticacion", "jwt"],
    decision_relacionada="id-de-decision-anterior"  # opcional
)
```

### Plantilla para Workflow de Debugging

```python
# Plantilla para workflow de debugging
def workflow_debugging(titulo, descripcion, archivos, etiquetas, solucion=None):
    try:
        # 1. Documentar el bug
        bug_id = m.create_entry(
            'bug',
            titulo,
            descripcion,
            etiquetas,
            files_affected=archivos,
            llm_context='Bug documentado para análisis y resolución'
        )
        
        print(f"✅ Bug documentado: {bug_id}")
        
        # 2. Si hay solución, documentarla como cambio
        if solucion:
            solucion_id = m.create_entry(
                'change',
                f"Solución para: {titulo}",
                solucion,
                etiquetas + ['solucion'],
                files_affected=archivos,
                related_entries=[bug_id],
                llm_context='Solución implementada para el bug documentado'
            )
            print(f"✅ Solución documentada: {solucion_id}")
        
        return bug_id
        
    except Exception as e:
        print(f"❌ Error al documentar bug: {e}")
        return None

# Ejemplo de uso
bug_id = workflow_debugging(
    titulo="Error en validación de parámetros",
    descripcion="Los parámetros opcionales no se validan correctamente...",
    archivos=["api/endpoints.py"],
    etiquetas=["bug", "validacion", "api"],
    solucion="Se implementó validación personalizada para parámetros opcionales..."
)
```

## 🚨 Plantilla para Manejo de Errores

```python
# Plantilla para manejo robusto de errores
def crear_entrada_segura(tipo, titulo, contenido, etiquetas=None, **kwargs):
    try:
        # Verificar que el proyecto esté inicializado
        if not hasattr(m, 'project_root') or not m.project_root.exists():
            print("❌ El proyecto no está inicializado")
            m.initialize_project()
            print("✅ Proyecto inicializado")
        
        # Crear la entrada
        entrada_id = m.create_entry(
            tipo,
            titulo,
            contenido,
            etiquetas,
            **kwargs
        )
        
        print(f"✅ Entrada creada exitosamente: {entrada_id}")
        return entrada_id
        
    except ValueError as e:
        print(f"❌ Error de validación: {e}")
        print("💡 Tipos válidos: decision, change, context, bug, feature, note")
        return None
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("🔧 Verifica la configuración del sistema")
        return None

# Ejemplo de uso seguro
entrada_id = crear_entrada_segura(
    'note',
    'Prueba de sistema',
    'Verificación de funcionamiento del sistema de memoria',
    ['test', 'verificacion']
)
```

## 📝 Plantilla para Comando de Prueba Completo

```python
# Comando completo de prueba para verificar funcionamiento
def prueba_completa_sistema():
    print("🧪 Iniciando prueba completa del sistema de memoria...")
    
    try:
        # 1. Importar e inicializar
        from memoria_cursor import MemorySystem
        m = MemorySystem('test-proyecto')
        m.initialize_project()
        print("✅ Sistema inicializado")
        
        # 2. Crear entrada de prueba
        test_id = m.create_entry(
            'note',
            'Prueba de funcionamiento del sistema',
            'Esta es una entrada de prueba para verificar que el sistema funciona correctamente. Incluye: inicialización, creación de entradas, y exportación.',
            ['test', 'verificacion', 'sistema']
        )
        print(f"✅ Entrada de prueba creada: {test_id}")
        
        # 3. Listar entradas
        entradas = m.list_entries()
        print(f"✅ Entradas listadas: {len(entradas)} encontradas")
        
        # 4. Exportar
        m.export_entries()
        print("✅ Memoria exportada")
        
        # 5. Limpiar (opcional)
        # m.delete_entry(test_id)
        # print("✅ Entrada de prueba eliminada")
        
        print("🎉 ¡Prueba completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

# Ejecutar prueba
if __name__ == "__main__":
    prueba_completa_sistema()
```

## 🎯 Resumen de Plantillas

**Plantillas Disponibles:**
1. **Inicialización**: Configuración básica del sistema
2. **Por Tipo**: Plantillas específicas para cada tipo de entrada
3. **Consultas**: Búsquedas y filtros de información
4. **Workflows**: Procesos completos de implementación y debugging
5. **Manejo de Errores**: Código robusto con validaciones
6. **Pruebas**: Verificación completa del sistema

**Uso Recomendado:**
- Copia la plantilla que necesites
- Adapta los parámetros a tu caso específico
- Usa las plantillas de manejo de errores para código robusto
- Ejecuta la prueba completa antes de usar en producción

Estas plantillas están diseñadas para ser copiadas directamente por agentes LLM y adaptadas a sus necesidades específicas.
