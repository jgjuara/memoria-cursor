# 🚀 Guía Rápida para Agentes LLM

## 🎯 ¿Eres un Agente LLM que necesita usar memoria-cursor?

**¡Perfecto! Este es tu punto de entrada.**

## 📚 Documentación Específica para LLMs

### 🚀 **PRIMERO: Lee la Guía Principal**
**[docs/llm-guide.md](llm-guide.md)** - Guía completa y específica para agentes LLM

### 📋 **SEGUNDO: Usa las Plantillas**
**[docs/llm-templates.md](llm-templates.md)** - Plantillas de código listas para copiar y adaptar

## ⚡ Inicio Rápido (3 Líneas)

```python
from memoria_cursor import MemorySystem
m = MemorySystem('nombre-proyecto')
m.initialize_project()
```

## 🚨 Errores Comunes que Debes Evitar

1. **❌ NO usar**: `from memoria_cursor import MemoriaCursor` (no existe)
2. **❌ NO olvidar**: `m.initialize_project()` (siempre requerido)
3. **❌ NO confundir**: El orden es `tipo`, `título`, `contenido`, `etiquetas`
4. **❌ NO usar tipos inválidos**: Solo `decision`, `change`, `context`, `bug`, `feature`, `note`

## 🔧 Comando de Prueba

```python
from memoria_cursor import MemorySystem
m = MemorySystem('test-proyecto')
m.initialize_project()
m.create_entry('note', 'Prueba', 'Verificación del sistema', ['test'])
```

## 📖 Documentación Completa

- **[Guía para LLMs](llm-guide.md)** ⭐ **OBLIGATORIO**
- **[Plantillas](llm-templates.md)** ⭐ **MUY ÚTIL**
- **[API Python](api-python.md)** - Referencia técnica completa
- **[Ejemplos](ejemplos.md)** - Casos de uso prácticos

## 🎯 Resumen para LLMs

**Siempre recuerda:**
1. Importar `MemorySystem` (no `MemoriaCursor`)
2. Llamar `initialize_project()` antes de todo
3. Usar tipos válidos: `decision`, `change`, `context`, `bug`, `feature`, `note`
4. Orden correcto: `tipo`, `título`, `contenido`, `etiquetas`

**¡Con esta documentación específica para LLMs, no deberías tener más errores!**
