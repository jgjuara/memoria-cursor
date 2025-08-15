# Ejemplos de Uso - Sistema de Memoria

## Ejemplos por Tipo de Entrada

### 1. Decisiones de Arquitectura

#### Elección de Base de Datos
```bash
memoria create decision "Elección de PostgreSQL como base de datos principal" "Se eligió PostgreSQL por su robustez ACID, soporte JSON nativo, capacidades de consulta avanzadas y excelente rendimiento para cargas de trabajo complejas. Alternativas consideradas: MongoDB (menos consistencia ACID), MySQL (limitaciones en JSON), SQLite (limitaciones de concurrencia). Esta decisión afecta toda la arquitectura de persistencia del sistema." --tags "arquitectura" "base-datos" "postgresql" "decision-tecnica"
```

#### Patrón de Diseño
```bash
memoria create decision "Implementación de Repository Pattern" "Se implementó el patrón Repository para abstraer la capa de acceso a datos. Esto permite cambiar la implementación de la base de datos sin afectar la lógica de negocio. Beneficios: testabilidad mejorada, desacoplamiento, flexibilidad para cambios futuros." --files "models.py" "repositories.py" "services.py" --tags "patron-diseno" "repository" "arquitectura"
```

#### Implementación Basada en Decisión Anterior
```bash
memoria create change "Implementación de Repository Pattern" "Se implementó el patrón Repository según la decisión de arquitectura anterior. Se crearon las clases base y las implementaciones específicas para PostgreSQL y MongoDB." --files "repositories/base.py" "repositories/postgresql.py" "repositories/mongodb.py" --related-entries "550e8400-e29b-41d4-a716-446655440000" --tags "implementacion" "repository" "postgresql" "mongodb"
```

### 2. Cambios Importantes en el Código

#### Refactoring de Autenticación
```bash
memoria create change "Migración de sesiones a JWT tokens" "Se migró el sistema de autenticación de sesiones basadas en servidor a JWT tokens. Motivo: mejorar escalabilidad para APIs y soporte de aplicaciones móviles. Cambios principales: auth.py (nueva lógica JWT), middleware.py (validación de tokens), models.py (eliminación de campos de sesión). Impacto: mejor rendimiento, mayor escalabilidad, soporte para microservicios." --files "auth.py" "middleware.py" "models.py" "config.py" --tags "refactoring" "autenticacion" "jwt" "escalabilidad"
```

#### Cambio en API
```bash
memoria create change "Actualización de API de usuarios v1 a v2" "Se actualizó la API de usuarios de v1 a v2 para incluir nuevos campos y mejorar la estructura de respuesta. Cambios: nuevos endpoints, campos adicionales (profile_image, preferences), paginación mejorada, filtros avanzados. Breaking changes documentados en API_DOCS.md." --files "api/users.py" "serializers.py" "tests/test_users.py" "API_DOCS.md" --tags "api" "versioning" "breaking-change"
```

### 3. Contexto del Proyecto

#### Configuración del Entorno
```bash
memoria create context "Configuración del entorno de desarrollo" "El proyecto requiere Python 3.8+, PostgreSQL 12+, Redis 6+, y Node.js 16+. Variables de entorno críticas: DATABASE_URL, REDIS_URL, SECRET_KEY, API_KEY. Configuración en .env.example. Para desarrollo local: docker-compose up -d postgres redis. Comandos de setup: pip install -r requirements.txt, npm install, python manage.py migrate." --tags "configuracion" "entorno" "dependencias" "setup"
```

#### Estado Actual del Proyecto
```bash
memoria create context "Estado actual del proyecto - Sprint 3" "Proyecto en fase de desarrollo activo. Sprint 3 enfocado en implementación de autenticación y autorización. Módulos completados: usuarios, autenticación, permisos básicos. En progreso: sistema de roles, API de administración. Próximos sprints: integración con servicios externos, optimización de rendimiento." --tags "estado" "sprint" "progreso" "roadmap"
```

### 4. Bugs y Problemas

#### Bug de Concurrencia
```bash
memoria create bug "Race condition en procesamiento de pagos" "Se identificó y resolvió race condition en el procesamiento de pagos cuando múltiples usuarios intentaban pagar simultáneamente. Síntomas: transacciones duplicadas, inconsistencias en saldos. Solución: implementación de locks optimistas y retry logic. Archivos modificados: payment_processor.py, models.py. Commit: a1b2c3d. Testing: agregados tests de concurrencia." --files "payment_processor.py" "models.py" "tests/test_payments.py" --tags "bug" "concurrencia" "transacciones" "resuelto"
```

#### Problema de Rendimiento
```bash
memoria create bug "Lentitud en consultas de reportes" "Se identificó problema de rendimiento en consultas de reportes con grandes volúmenes de datos. Causa: falta de índices en tablas de transacciones y consultas N+1. Solución: agregados índices compuestos, implementado eager loading, optimizadas consultas. Mejora: 80% reducción en tiempo de respuesta. Monitoreo: agregado logging de performance." --files "reports.py" "models.py" "migrations/" --tags "performance" "optimizacion" "base-datos" "resuelto"
```

### 5. Nuevas Funcionalidades

#### Implementación de Notificaciones
```bash
memoria create feature "Sistema de notificaciones push" "Se implementó sistema completo de notificaciones push para aplicaciones móviles. Funcionalidades: notificaciones en tiempo real, templates personalizables, programación de notificaciones, analytics de engagement. Tecnologías: Firebase Cloud Messaging, WebSockets, Redis para colas. Archivos: notifications.py, templates/, mobile_api/. Testing: cobertura 95%." --files "notifications.py" "templates/" "mobile_api/" "tests/test_notifications.py" --tags "feature" "notificaciones" "mobile" "real-time"
```

#### Dashboard de Analytics
```bash
memoria create feature "Dashboard de analytics en tiempo real" "Se desarrolló dashboard de analytics con métricas en tiempo real. Funcionalidades: gráficos interactivos, filtros dinámicos, exportación de datos, alertas automáticas. Tecnologías: Chart.js, WebSockets, Redis para cache. Integración con Google Analytics y herramientas internas. Archivos: analytics/, dashboard/, frontend/components/." --files "analytics/" "dashboard/" "frontend/components/" --tags "feature" "analytics" "dashboard" "real-time"
```

### 6. Notas Generales

#### Observación de Rendimiento
```bash
memoria create note "Observación sobre uso de memoria en producción" "Se observó alto uso de memoria en servidores de producción durante picos de tráfico. Análisis: cache de Redis no se está limpiando correctamente, sesiones acumulándose. Solución temporal: restart diario de servicios. Solución permanente: implementar TTL en cache, limpieza automática de sesiones. Monitoreo: agregar alertas de memoria." --tags "observacion" "performance" "memoria" "produccion"
```

#### Nota de Implementación
```bash
memoria create note "Consideraciones para futuras implementaciones" "Para futuras implementaciones de APIs, considerar desde el inicio: versioning, documentación automática (Swagger), rate limiting, logging estructurado, métricas de performance. Esto evitará refactoring costoso posterior. Referencia: ver implementación actual de API v2 que requirió cambios significativos." --tags "nota" "implementacion" "mejores-practicas" "futuro"
```

## Ejemplos de Consultas y Búsquedas

### Buscar Decisiones Recientes
```bash
memoria list --type decision --limit 5
```

### Buscar Cambios Relacionados con API
```bash
memoria list --search "api" --type change
```

### Ver Entradas con Información de Git
```bash
memoria list --show-git --limit 10
```

### Buscar por Etiquetas Específicas
```bash
memoria list --tags "arquitectura" "base-datos"
```

### Ver Estadísticas del Proyecto
```bash
memoria list --stats
```

## Ejemplos de Exportación

### Exportar Solo Decisiones para Revisión
```bash
memoria list --type decision | memoria export --format markdown
```

### Exportar Cambios Recientes para LLM
```bash
memoria list --type change --limit 20 | memoria export --format json
```

### Exportar Contexto Completo
```bash
memoria export --format markdown --group-by date
```

## Ejemplos de Workflow Completo

### Workflow para Nueva Funcionalidad

1. **Registrar decisión de implementación**:
```bash
memoria create decision "Implementación de sistema de búsqueda" "Se decidió implementar búsqueda full-text con Elasticsearch para mejorar experiencia de usuario. Alternativas: PostgreSQL full-text search (limitado), Algolia (costoso). Elasticsearch elegido por flexibilidad y escalabilidad." --tags "decision" "busqueda" "elasticsearch"
```

2. **Registrar cambios durante implementación** (referenciando la decisión):
```bash
memoria create change "Configuración inicial de Elasticsearch" "Se configuró cluster de Elasticsearch con 3 nodos, índices optimizados para búsqueda de productos. Archivos: elasticsearch.yml, mappings.json, docker-compose.override.yml" --files "elasticsearch.yml" "mappings.json" "docker-compose.override.yml" --related-entries "550e8400-e29b-41d4-a716-446655440000" --tags "implementacion" "elasticsearch" "configuracion"
```

3. **Registrar bug encontrado** (referenciando la implementación):
```bash
memoria create bug "Problema de sincronización de datos" "Se encontró problema de sincronización entre PostgreSQL y Elasticsearch. Causa: falta de triggers para actualización automática. Solución: implementado sistema de eventos con Redis pub/sub." --files "sync_service.py" "triggers.sql" --related-entries "6ba7b810-9dad-11d1-80b4-00c04fd430c8" --tags "bug" "sincronizacion" "elasticsearch"
```

4. **Registrar funcionalidad completada** (referenciando la decisión y el bug):
```bash
memoria create feature "Sistema de búsqueda implementado" "Sistema de búsqueda full-text completamente funcional. Funcionalidades: búsqueda por texto, filtros avanzados, autocompletado, ranking personalizado. Performance: <100ms para consultas complejas. Testing: 90% cobertura." --files "search_service.py" "api/search.py" "frontend/search.js" --related-entries "550e8400-e29b-41d4-a716-446655440000" "6ba7b810-9dad-11d1-80b4-00c04fd430c8" --tags "feature" "busqueda" "completado"
```

### Workflow para Resolución de Bug

1. **Registrar bug reportado**:
```bash
memoria create bug "Error 500 en endpoint de usuarios" "Usuarios reportan error 500 al acceder a /api/users. Error ocurre en producción con alta carga. Prioridad: alta. Necesita investigación inmediata." --tags "bug" "produccion" "api" "critico"
```

2. **Registrar investigación** (referenciando el bug):
```bash
memoria create note "Investigación del error 500" "Análisis de logs muestra timeout en consulta de base de datos. Consulta afectada: SELECT * FROM users WHERE status = 'active'. Problema: falta índice en columna status. Solución: agregar índice." --related-entries "9ba7b810-9dad-11d1-80b4-00c04fd430c8" --tags "investigacion" "debugging" "base-datos"
```

3. **Registrar solución implementada** (referenciando el bug y la investigación):
```bash
memoria create change "Agregado índice para resolver error 500" "Se agregó índice en columna status de tabla users. Migración: 001_add_user_status_index.sql. Testing: verificado que resuelve el timeout. Deploy: aplicado en producción." --files "migrations/001_add_user_status_index.sql" --related-entries "9ba7b810-9dad-11d1-80b4-00c04fd430c8" "cba7b810-9dad-11d1-80b4-00c04fd430c8" --tags "fix" "indice" "base-datos" "resuelto"
```

## Ejemplos de Configuración Avanzada

### Script Personalizado para Decisiones
```bash
#!/bin/bash
# scripts/record-decision.sh
memoria create decision "$1" "$2" --tags "${3:-decision}" --llm-context "Esta decisión afecta la arquitectura del sistema y debe considerarse en futuras implementaciones"
```

### Script para Cambios de Código
```bash
#!/bin/bash
# scripts/record-change.sh
memoria create change "$1" "$2" --files "$3" --tags "${4:-change}" --llm-context "Este cambio modifica la funcionalidad existente y puede requerir actualización de documentación"
```

### Alias Útiles
```bash
# Agregar a .bashrc o .zshrc
alias memoria-decision='memoria create decision'
alias memoria-change='memoria create change'
alias memoria-bug='memoria create bug'
alias memoria-feature='memoria create feature'
alias memoria-context='memoria create context'
alias memoria-note='memoria create note'
alias memoria-list='memoria list'
alias memoria-export='memoria export'
alias memoria-stats='memoria list --stats'
```

## Ejemplos de Integración con CI/CD

### Script de Pre-commit
```bash
#!/bin/bash
# .git/hooks/pre-commit
# Verificar que cambios importantes estén documentados
if git diff --cached --name-only | grep -E "\.(py|js|ts)$" > /dev/null; then
    echo "⚠️  Considera registrar cambios importantes con: memoria create"
fi
```

### Script de Post-deploy
```bash
#!/bin/bash
# scripts/post-deploy.sh
# Registrar deploy en memoria
memoria create note "Deploy completado - $(date)" "Deploy exitoso a producción. Versión: $VERSION. Cambios incluidos: $CHANGES" --tags "deploy" "produccion"
```

Estos ejemplos muestran cómo usar el sistema de memoria de manera efectiva en diferentes escenarios del desarrollo de software.
