"""
Herramienta para listar y buscar entradas en el sistema de memoria.
"""

from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from datetime import datetime

from ..core.memory_system import MemorySystem
from ..core.entry import Entry


def list_entries(project_root: str = ".",
                limit: Optional[int] = None,
                offset: int = 0,
                entry_type: Optional[str] = None,
                tags: Optional[List[str]] = None,
                search: Optional[str] = None,
                date_from: Optional[str] = None,
                date_to: Optional[str] = None,
                show_git: bool = False,
                stats: bool = False) -> List[Entry]:
    """
    Listar entradas del sistema de memoria con filtros opcionales.
    
    Args:
        project_root: Ruta raíz del proyecto
        limit: Número máximo de entradas a retornar
        offset: Número de entradas a omitir desde el inicio (para paginación)
        entry_type: Filtrar por tipo de entrada
        tags: Filtrar por etiquetas
        search: Buscar en título y contenido
        date_from: Fecha de inicio (YYYY-MM-DD)
        date_to: Fecha de fin (YYYY-MM-DD)
        show_git: Mostrar información de Git
        stats: Mostrar estadísticas en lugar de entradas
        
    Returns:
        Lista de entradas filtradas
    """
    # Inicializar sistema de memoria
    memory_system = MemorySystem(project_root)
    
    if stats:
        return _get_statistics(memory_system)
    
    # Obtener entradas filtradas
    entries = memory_system.list_entries(
        limit=limit,
        offset=offset,
        entry_type=entry_type,
        tags=tags,
        search=search,
        date_from=date_from,
        date_to=date_to
    )
    
    return entries


def display_entries(entries: List[Entry], 
                   show_git: bool = False,
                   limit: Optional[int] = None,
                   offset: int = 0) -> None:
    """
    Mostrar entradas en formato de lista usando print para evitar problemas de consola.
    
    Args:
        entries: Lista de entradas a mostrar
        show_git: Mostrar información de Git
        limit: Número máximo de entradas a mostrar
        offset: Número de entradas omitidas desde el inicio
    """
    if not entries:
        console = Console()
        console.print(Panel("No se encontraron entradas", style="yellow"))
        return
    
    # Aplicar límite si se especifica
    if limit:
        entries = entries[-limit:]
    
    # Mostrar título
    print("\n📚 Entradas de Memoria")
    print("=" * 50)
    
    # Mostrar información de paginación si hay offset
    if offset > 0:
        print(f"📍 Mostrando desde la entrada #{offset + 1}")
    if limit:
        print(f"📄 Mostrando máximo {limit} entradas")
    if offset > 0 or limit:
        print()
    
    # Mostrar cada entrada en formato de lista
    for i, entry in enumerate(entries):
        # Separador entre entradas
        if i > 0:
            print("\n" + "─" * 50)
        
        # ID completo
        print(f"ID: {entry.entry_id}")
        
        # Tipo
        print(f"Tipo: {entry.entry_type.upper()}")
        
        # Título completo
        print(f"Título: {entry.title}")
        
        # Fecha
        try:
            dt = datetime.fromisoformat(entry.timestamp)
            formatted_date = dt.strftime("%Y-%m-%d %H:%M")
        except ValueError:
            formatted_date = entry.timestamp[:16] if entry.timestamp else "N/A"
        print(f"Fecha: {formatted_date}")
        
        # Etiquetas
        if entry.tags:
            tags_str = ", ".join(entry.tags)
            print(f"Etiquetas: {tags_str}")
        else:
            print("Etiquetas: Ninguna")
        
        # Archivos afectados
        if entry.files_affected:
            files_str = ", ".join(entry.files_affected)
            print(f"Archivos: {files_str}")
        
        # Entradas relacionadas
        if entry.related_entries:
            related_str = ", ".join(entry.related_entries)
            print(f"Relacionadas: {related_str}")
        
        # Contenido truncado para vista previa
        if entry.content:
            # Truncar contenido a ~120 caracteres para mantener formato limpio
            content_preview = entry.content.strip()
            if len(content_preview) > 120:
                content_preview = content_preview[:117] + "..."
            print(f"Contenido: {content_preview}")
        
        # Información de Git si se solicita
        if show_git and entry.git_info:
            git_info = entry.git_info
            print(f"Git Commit: {git_info.get('current_commit', 'N/A')}")
            print(f"Git Rama: {git_info.get('branch', 'N/A')}")
            if git_info.get('commit_message'):
                print(f"Git Mensaje: {git_info.get('commit_message', 'N/A')}")
    
    # Mostrar resumen
    print(f"\n📊 Total de entradas mostradas: {len(entries)}")


def display_entry_details(entry: Entry, show_git: bool = False) -> None:
    """
    Mostrar detalles completos de una entrada.
    
    Args:
        entry: Entrada a mostrar
        show_git: Mostrar información de Git
    """
    console = Console()
    
    # Crear panel principal
    content = f"""
[bold]Título:[/bold] {entry.title}
[bold]Tipo:[/bold] {entry.entry_type.upper()}
[bold]ID:[/bold] {entry.entry_id}
[bold]Fecha:[/bold] {entry.timestamp}
[bold]Etiquetas:[/bold] {', '.join(entry.tags) if entry.tags else 'Ninguna'}
[bold]Archivos afectados:[/bold] {', '.join(entry.files_affected) if entry.files_affected else 'Ninguno'}
[bold]Entradas relacionadas:[/bold] {', '.join(entry.related_entries) if entry.related_entries else 'Ninguna'}

[bold]Contenido:[/bold]
{entry.content}
"""
    
    if entry.llm_context:
        content += f"\n[bold]Contexto LLM:[/bold]\n{entry.llm_context}"
    
    if show_git and entry.git_info:
        git_info = entry.git_info
        content += f"""
[bold]Información Git:[/bold]
  Commit: {git_info.get('current_commit', 'N/A')}
  Rama: {git_info.get('branch', 'N/A')}
  Mensaje: {git_info.get('commit_message', 'N/A')}
  Estado: {'Limpio' if git_info.get('is_clean') else 'Con cambios'}
"""
    
    panel = Panel(content, title=f"📝 Entrada {entry.entry_id}", border_style="blue")
    console.print(panel)


def _get_statistics(memory_system: MemorySystem) -> List[Entry]:
    """
    Obtener y mostrar estadísticas del sistema.
    
    Args:
        memory_system: Sistema de memoria
        
    Returns:
        Lista vacía (solo para compatibilidad con la interfaz)
    """
    stats = memory_system.get_statistics()
    
    console = Console()
    
    # Mostrar título
    console.print("\n📊 Estadísticas del Sistema de Memoria", style="bold magenta")
    console.print("=" * 50)
    
    # Estadísticas básicas
    console.print(f"Total de entradas: {stats.get('total_entries', 0)}", style="bold")
    created = stats.get("created", "N/A")
    if created != "N/A":
        created = created[:10]
    console.print(f"Fecha de creación: {created}")
    
    last_updated = stats.get("last_updated", "N/A")
    if last_updated != "N/A":
        last_updated = last_updated[:10]
    console.print(f"Última actualización: {last_updated}")
    
    # Estadísticas por tipo
    by_type = stats.get("by_type", {})
    if by_type:
        console.print("\n[bold]Distribución por tipo:[/bold]")
        for entry_type, count in sorted(by_type.items()):
            console.print(f"  {entry_type}: {count}")
    
    # Total de etiquetas únicas
    total_tags = stats.get("total_tags", [])
    console.print(f"\nEtiquetas únicas: {len(total_tags)}")
    
    if total_tags:
        console.print("[bold]Lista de etiquetas:[/bold]")
        # Agrupar etiquetas por líneas
        tags_per_line = 5
        for i in range(0, len(total_tags), tags_per_line):
            line_tags = total_tags[i:i + tags_per_line]
            console.print(f"  {', '.join(line_tags)}")
    
    # Mostrar gráfico de barras simple para tipos
    if by_type:
        console.print("\n[bold]Distribución por tipo:[/bold]")
        max_count = max(by_type.values()) if by_type.values() else 1
        
        for entry_type, count in sorted(by_type.items()):
            bar_length = int((count / max_count) * 30)
            bar = "█" * bar_length
            percentage = (count / stats.get("total_entries", 1)) * 100
            console.print(f"{entry_type:12} {bar} {count:3} ({percentage:5.1f}%)")
    
    return []  # Retornar lista vacía para compatibilidad


def search_entries_interactive(project_root: str = ".") -> None:
    """
    Búsqueda interactiva de entradas.
    
    Args:
        project_root: Ruta raíz del proyecto
    """
    console = Console()
    console.print("🔍 Búsqueda interactiva de entradas", style="bold blue")
    console.print("=" * 50)
    
    # Inicializar sistema
    memory_system = MemorySystem(project_root)
    
    while True:
        console.print("\nOpciones de búsqueda:")
        console.print("1. Buscar por texto")
        console.print("2. Filtrar por tipo")
        console.print("3. Filtrar por etiquetas")
        console.print("4. Filtrar por fecha")
        console.print("5. Ver estadísticas")
        console.print("6. Salir")
        
        choice = input("\nSelecciona una opción (1-6): ").strip()
        
        if choice == "1":
            search_term = input("Término de búsqueda: ").strip()
            if search_term:
                entries = memory_system.list_entries(search=search_term)
                display_entries(entries)
        
        elif choice == "2":
            console.print("\nTipos disponibles: decision, change, context, bug, feature, note")
            entry_type = input("Tipo de entrada: ").strip().lower()
            if entry_type:
                entries = memory_system.list_entries(entry_type=entry_type)
                display_entries(entries)
        
        elif choice == "3":
            tags_input = input("Etiquetas (separadas por comas): ").strip()
            if tags_input:
                tags = [tag.strip() for tag in tags_input.split(",")]
                entries = memory_system.list_entries(tags=tags)
                display_entries(entries)
        
        elif choice == "4":
            date_from = input("Fecha desde (YYYY-MM-DD): ").strip()
            date_to = input("Fecha hasta (YYYY-MM-DD): ").strip()
            if date_from or date_to:
                entries = memory_system.list_entries(date_from=date_from, date_to=date_to)
                display_entries(entries)
        
        elif choice == "5":
            _get_statistics(memory_system)
        
        elif choice == "6":
            console.print("👋 ¡Hasta luego!")
            break
        
        else:
            console.print("❌ Opción inválida. Intenta de nuevo.", style="red")
