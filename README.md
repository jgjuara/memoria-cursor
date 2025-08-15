# Sistema de Memoria para Agentes LLM

Una herramienta sencilla, liviana y portable para registrar información relevante del desarrollo de proyectos que puede alimentar las interacciones con agentes LLM (Cursor, Claude Code, etc.).

## 🚀 Instalación

### Como Módulo Python (Recomendado)

```bash
# Instalación desde PyPI (cuando esté disponible)
pip install memoria-cursor

# Instalación desde fuente
git clone https://github.com/tu-usuario/memoria-cursor.git
cd memoria-cursor
pip install -e .

# Instalación usando uv (más rápido)
uv pip install git+https://github.com/tu-usuario/memoria-cursor.git
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
# 1. Instalar el módulo
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
memoria create change "Implementación de autenticación" "Sistema JWT agregado" --files "auth.py" "models.py"

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

# Exportar solo decisiones
memoria list --type decision | memoria export
```

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

- **[Guía de Uso](docs/guia-uso.md)** - Documentación completa
- **[Ejemplos](docs/ejemplos.md)** - Casos de uso prácticos
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