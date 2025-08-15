"""
Herramienta para crear entradas en el sistema de memoria.
"""

from typing import List, Optional
from ..core.memory_system import MemorySystem


def create_entry(project_root: str = ".",
                entry_type: str = "note",
                title: str = "",
                content: str = "",
                tags: Optional[List[str]] = None,
                files_affected: Optional[List[str]] = None,
                llm_context: Optional[str] = None,
                related_entries: Optional[List[str]] = None) -> str:
    """
    Crear una nueva entrada en el sistema de memoria.
    
    Args:
        project_root: Ruta raíz del proyecto
        entry_type: Tipo de entrada (decision, change, context, bug, feature, note)
        title: Título descriptivo de la entrada
        content: Contenido principal de la entrada
        tags: Lista de etiquetas para categorización
        files_affected: Lista de archivos afectados
        llm_context: Contexto específico para agentes LLM
        related_entries: Lista de IDs de entradas relacionadas para contexto
        
    Returns:
        ID de la entrada creada
        
    Raises:
        ValueError: Si el tipo de entrada es inválido o faltan campos requeridos
    """
    # Validar campos requeridos
    if not title.strip():
        raise ValueError("El título es obligatorio")
    
    if not content.strip():
        raise ValueError("El contenido es obligatorio")
    
    # Validar tipo de entrada
    valid_types = ["decision", "change", "context", "bug", "feature", "note"]
    if entry_type not in valid_types:
        raise ValueError(f"Tipo de entrada inválido. Debe ser uno de: {valid_types}")
    
    # Inicializar sistema de memoria
    memory_system = MemorySystem(project_root)
    
    # Crear entrada
    entry_id = memory_system.create_entry(
        entry_type=entry_type,
        title=title.strip(),
        content=content.strip(),
        tags=tags or [],
        files_affected=files_affected or [],
        llm_context=llm_context.strip() if llm_context else None,
        related_entries=related_entries or []
    )
    
    return entry_id


def create_entry_interactive(project_root: str = ".") -> str:
    """
    Crear entrada de forma interactiva solicitando datos al usuario.
    
    Args:
        project_root: Ruta raíz del proyecto
        
    Returns:
        ID de la entrada creada
    """
    print("📝 Crear nueva entrada de memoria")
    print("=" * 40)
    
    # Solicitar tipo de entrada
    print("\nTipos disponibles:")
    types_info = {
        "decision": "Decisiones de arquitectura y diseño",
        "change": "Cambios importantes en el código",
        "context": "Información de contexto del proyecto",
        "bug": "Problemas y bugs encontrados",
        "feature": "Nuevas funcionalidades implementadas",
        "note": "Notas generales y observaciones"
    }
    
    for entry_type, description in types_info.items():
        print(f"  {entry_type}: {description}")
    
    while True:
        entry_type = input("\nTipo de entrada: ").strip().lower()
        if entry_type in types_info:
            break
        print("❌ Tipo inválido. Intenta de nuevo.")
    
    # Solicitar título
    while True:
        title = input("\nTítulo de la entrada: ").strip()
        if title:
            break
        print("❌ El título es obligatorio.")
    
    # Solicitar contenido
    print("\nContenido de la entrada (presiona Enter dos veces para terminar):")
    content_lines = []
    while True:
        line = input()
        if line == "" and content_lines and content_lines[-1] == "":
            break
        content_lines.append(line)
    
    content = "\n".join(content_lines[:-1])  # Remover línea vacía final
    
    if not content.strip():
        print("❌ El contenido es obligatorio.")
        return None
    
    # Solicitar etiquetas
    tags_input = input("\nEtiquetas (separadas por comas): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []
    
    # Solicitar archivos afectados
    files_input = input("\nArchivos afectados (separados por comas): ").strip()
    files_affected = [file.strip() for file in files_input.split(",") if file.strip()] if files_input else []
    
    # Solicitar contexto LLM
    llm_context = input("\nContexto específico para LLM (opcional): ").strip()
    if not llm_context:
        llm_context = None
    
    # Solicitar entradas relacionadas
    related_input = input("\nIDs de entradas relacionadas (separados por comas): ").strip()
    related_entries = [entry_id.strip() for entry_id in related_input.split(",") if entry_id.strip()] if related_input else []
    
    # Crear entrada
    try:
        entry_id = create_entry(
            project_root=project_root,
            entry_type=entry_type,
            title=title,
            content=content,
            tags=tags,
            files_affected=files_affected,
            llm_context=llm_context,
            related_entries=related_entries
        )
        
        print(f"\n✅ Entrada creada exitosamente con ID: {entry_id}")
        return entry_id
        
    except Exception as e:
        print(f"\n❌ Error al crear entrada: {e}")
        return None
