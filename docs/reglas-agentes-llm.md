# Reglas para Agentes LLM - Sistema de Memoria

## Uso Obligatorio del Sistema

### Cuando Registrar Información

**SIEMPRE registrar cuando:**
- Se toman decisiones de arquitectura o diseño
- Se implementan cambios significativos en el código
- Se resuelven bugs o problemas importantes
- Se agregan nuevas funcionalidades
- Se cambia la configuración del proyecto
- Se documenta contexto relevante para futuras interacciones

### Comando de Registro

**Usar SIEMPRE este comando para registrar:**
```bash
memoria create <tipo> "<titulo>" "<contenido>" [opciones]
```

### Tipos de Entradas

1. **`decision`** - Decisiones de arquitectura y diseño
   - Elección de tecnologías
   - Patrones de diseño implementados
   - Decisiones de estructura de datos

2. **`change`** - Cambios importantes en el código
   - Refactoring significativo
   - Cambios en APIs
   - Modificaciones de estructura

3. **`context`** - Información de contexto del proyecto
   - Configuración del entorno
   - Dependencias importantes
   - Estado actual del proyecto

4. **`bug`** - Problemas y bugs encontrados
   - Bugs resueltos
   - Problemas de rendimiento
   - Limitaciones identificadas

5. **`feature`** - Nuevas funcionalidades implementadas
   - Características agregadas
   - Mejoras implementadas
   - Nuevas capacidades

6. **`note`** - Notas generales y observaciones
   - Observaciones importantes
   - Notas de implementación
   - Comentarios relevantes

## Ejemplos de Uso

### Registrar una Decisión
```bash
memoria create decision "Elección de base de datos" "Se eligió PostgreSQL por su robustez, soporte JSON nativo y capacidades de consulta avanzadas. Alternativas consideradas: MongoDB (menos ACID) y SQLite (limitaciones de concurrencia)." --tags "arquitectura" "base-datos" "postgresql"
```

### Registrar un Cambio Importante
```bash
memoria create change "Refactoring de autenticación" "Se migró de sistema de sesiones a JWT tokens para mejorar escalabilidad y soporte de APIs. Archivos modificados: auth.py, models.py, middleware.py" --files "auth.py" "models.py" "middleware.py" --tags "refactoring" "autenticacion" "jwt"
```

### Registrar Contexto del Proyecto
```bash
memoria create context "Configuración del entorno de desarrollo" "El proyecto requiere Python 3.8+, PostgreSQL 12+, y Redis 6+. Variables de entorno críticas: DATABASE_URL, REDIS_URL, SECRET_KEY. Configuración en .env.example" --tags "configuracion" "entorno" "dependencias"
```

### Registrar un Bug Resuelto
```bash
memoria create bug "Problema de concurrencia en transacciones" "Se identificó y resolvió race condition en procesamiento de pagos. Solución: implementación de locks optimistas y retry logic. Commit: a1b2c3d" --tags "bug" "concurrencia" "transacciones" --files "payment_processor.py"
```

## Opciones Adicionales

### Etiquetas (--tags)
Usar etiquetas relevantes para categorizar:
```bash
--tags "arquitectura" "performance" "seguridad"
```

### Archivos Afectados (--files)
Listar archivos relevantes:
```bash
--files "models.py" "views.py" "config.py"
```

### Entradas Relacionadas (--related-entries)
Referenciar entradas anteriores para contexto:
```bash
--related-entries "550e8400-e29b-41d4-a716-446655440000" "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
```

### Contexto LLM (--llm-context)
Información específica para agentes LLM:
```bash
--llm-context "Esta decisión afecta la escalabilidad del sistema y debe considerarse en futuras implementaciones"
```

## Consulta de Información

### Listar Entradas Recientes
```bash
memoria list --limit 10
```

### Buscar por Tipo
```bash
memoria list --type decision
```

### Buscar por Etiquetas
```bash
memoria list --tags "arquitectura" "base-datos"
```

### Buscar por Contenido
```bash
memoria list --search "postgresql"
```

### Ver Estadísticas
```bash
memoria list --stats
```

## Exportación para LLM

### Exportar para Compartir con Agentes
```bash
memoria export --format markdown
```

### Exportar Solo Decisiones
```bash
memoria list --type decision | memoria export --format json
```

## Integración Automática con Git

El sistema captura automáticamente:
- **Commit actual**: Hash del commit en el que se registra la entrada
- **Rama**: Rama de trabajo actual
- **Estado**: Si el repositorio está limpio o con cambios pendientes
- **Mensaje**: Mensaje del commit actual

## Reglas Específicas para Agentes

### Antes de Implementar Cambios
1. Revisar entradas recientes: `memoria list --limit 5`
2. Buscar decisiones relacionadas: `memoria list --type decision --search "palabra-clave"`
3. Verificar contexto del proyecto: `memoria list --type context`
4. **Revisar entradas relacionadas** de las decisiones encontradas para entender el contexto completo

### Después de Implementar Cambios
1. Registrar la implementación: `memoria create change "Descripción" "Detalles"`
2. Incluir archivos afectados: `--files "archivo1.py" "archivo2.py"`
3. Agregar etiquetas relevantes: `--tags "categoria1" "categoria2"`
4. **Referenciar entradas relacionadas**: `--related-entries "ID1" "ID2"` para conectar con decisiones o cambios anteriores

### Después de Implementar Cambios
1. Registrar la implementación: `memoria create change "Descripción" "Detalles"`
2. Incluir archivos afectados: `--files "archivo1.py" "archivo2.py"`
3. Agregar etiquetas relevantes: `--tags "categoria1" "categoria2"`

### Para Decisiones Importantes
1. Registrar la decisión: `memoria create decision "Título" "Justificación"`
2. Incluir alternativas consideradas
3. Explicar el razonamiento
4. Agregar contexto para futuras referencias

## Mejores Prácticas

1. **Ser específico**: Incluir detalles técnicos relevantes
2. **Usar etiquetas**: Facilitar búsquedas futuras
3. **Referenciar archivos**: Conectar entradas con código específico
4. **Incluir contexto**: Explicar el "por qué" además del "qué"
5. **Mantener consistencia**: Usar el mismo formato y estructura
6. **Actualizar regularmente**: Registrar información mientras está fresca

## Comandos de Conveniencia

### Alias Recomendados (agregar a .bashrc o .zshrc)
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
```
