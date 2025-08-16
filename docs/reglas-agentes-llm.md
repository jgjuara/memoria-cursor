## Reglas obligatorias para uso de memoria-cursor por agentes LLM

- **Uso obligatorio del módulo**
  - Todo proyecto debe usar `memoria-cursor`. Antes de comenzar, leer `docs/llm-guide.md` y `docs/llm-templates.md`.

- **Inicio de sesión de trabajo (antes de tocar código)**
  - Ejecutar `memoria status`. Si el sistema no está inicializado, ejecutar `memoria init` y crear una entrada `context` con el setup realizado.
  - Revisar contexto reciente: `memoria list --type decision --limit 10`, `memoria list --type context --limit 10` y `memoria list --search "<palabra-clave>"`.

- **Registro de cambios (obligatorio)**
  - Cada edición/creación/eliminación de archivos debe registrarse con `memoria create` usando el tipo adecuado:
    - `decision`: decisiones de diseño/arquitectura (registrar antes de implementarlas).
    - `change`: cambios de código o estructura.
    - `feature`: nuevas funcionalidades.
    - `bug`: hallazgos/correcciones de errores.
    - `context`: información relevante no ligada a un cambio puntual.
    - `note`: observaciones generales.
  - En `change/feature/bug` es obligatorio indicar todos los archivos afectados con `--files`.

- **Vinculación con Git (sin modificar el árbol)**
  - No ejecutar comandos Git que modifiquen el árbol desde el agente. La integración capta HEAD, rama y limpieza automáticamente.
  - Asociar cada commit relevante a una entrada:
    - Preferido: crear la entrada inmediatamente después del commit para que `git_info.current_commit` refleje el hash correcto.
    - Al redactar mensajes de commit, incluir el ID de entrada: `mem:<ENTRY_ID>`.

- **Contenido mínimo de cada entrada**
  - Requeridos: `type`, `title` (≤200 chars), `content` (no vacío).
  - Para `change/feature/bug`: `--files` obligatorio.
  - `tags`: al menos 1 etiqueta (p.ej., `refactor`, `bugfix`, `perf`, `security`).
  - En `content`, incluir secciones breves: Acciones implementadas; Consideraciones/razón; Impacto y riesgos; Pruebas/verificación.
  - Usar `--related-entries` para vincular con decisiones/bugs previos.
  - `--llm-context`: 3–6 bullets con contexto útil para agentes futuros.

- **Frecuencia y granularidad**
  - Registrar tras cada cambio lógico y cohesivo. Si varios archivos cambian por el mismo motivo, una sola entrada con todos los `--files`.

- **Cierre de sesión (después de la tarea)**
  - Exportar resumen: `memoria export --summary` o `memoria export --group-by type --limit 50`.
  - Si no hubo entradas nuevas, crear `note` explicando por qué no se requirió registrar cambios.

- **Criterios de aceptación (rechazar si no se cumplen)**
  - Intentar editar código sin `memoria status` en la sesión.
  - `change/feature/bug` sin `--files`.
  - Entradas sin secciones mínimas en `content`.
  - Commit relevante sin entrada asociada en la sesión.

## Workflow de sesión recomendado

- **Antes de codear**
  - `memoria status`
  - `memoria list --type decision --limit 10`
  - `memoria list --type context --limit 10`
  - `memoria list --search "<palabra-clave>"`

- **Durante**
  - Decisión previa: `memoria create decision "Título" "Decisión, alternativas y justificación" --tags arquitectura`
  - Cambio de código: `memoria create change "Descripción" "Acciones; Motivación; Impacto; Pruebas" --files "ruta/archivo1.py" --files "ruta/archivo2.py" --tags refactor --related-entries "<id>"`
  - Bug: `memoria create bug "Resumen" "Pasos; Esperado; Actual; Fix" --files "ruta/archivo.py" --tags bugfix`

- **Después**
  - `memoria export --summary`
  - Opcional: `memoria export --group-by tags --chunked --max-tokens 3000`

## Plantillas rápidas (CLI)

```bash
# Decisión (antes de implementar)
memoria create decision "Título claro" "Decisión, alternativas y justificación" \
  --tags arquitectura --llm-context "Impacto/alcance; Riesgos; Supuestos"

# Cambio de código
memoria create change "Descripción breve en imperativo" "Acciones; Motivación; Impacto; Pruebas" \
  --files "ruta/archivo1.py" --files "ruta/archivo2.py" \
  --tags refactor --tags modulo-x \
  --related-entries "<id-decision-o-bug>" \
  --llm-context "Resumen para LLMs (3–6 bullets)"

# Exportar resumen de sesión
memoria export --summary
```

## Referencias

- `docs/llm-guide.md`: guía de inicio rápido y API.
- `docs/llm-templates.md`: plantillas listas para usar.
