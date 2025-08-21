"""
Interfaz de línea de comandos para el sistema de memoria.
"""

import click
import os
import traceback
from pathlib import Path
from typing import Optional, List

from .core.memory_system import MemorySystem
from .tools.create import create_entry, create_entry_interactive
from .tools.list import list_entries, display_entries, display_entry_details, search_entries_interactive
from .tools.export import LLMExporter
from . import __version__


@click.group()
@click.version_option(version=__version__, prog_name="memoria-cursor")
@click.option('--project-root', '-p', default='.', 
              help='Ruta raíz del proyecto (por defecto: directorio actual)')
@click.pass_context
def main(ctx, project_root):
    """
    Sistema de Memoria para Agentes LLM
    
    Una herramienta para registrar información relevante del desarrollo de proyectos
    que puede alimentar las interacciones con agentes LLM (Cursor, Claude Code, etc.).
    """
    ctx.ensure_object(dict)
    ctx.obj['PROJECT_ROOT'] = Path(project_root).resolve()


@main.command()
@click.argument('type')
@click.argument('title')
@click.argument('content')
@click.option('--tags', '-t', multiple=True, help='Etiquetas para la entrada')
@click.option('--files', '-f', multiple=True, help='Archivos afectados')
@click.option('--llm-context', '-l', help='Contexto específico para LLM')
@click.option('--related-entries', '-r', multiple=True, help='IDs de entradas relacionadas para contexto')
@click.option('--interactive', '-i', is_flag=True, help='Modo interactivo')
@click.pass_context
def create(ctx, type, title, content, tags, files, llm_context, related_entries, interactive):
    """Crear una nueva entrada en el sistema de memoria."""
    project_root = ctx.obj.get('PROJECT_ROOT') if ctx and ctx.obj else Path('.').resolve()
    
    if interactive:
        create_entry_interactive(project_root)
        return
    
    try:
        entry_id = create_entry(
            project_root=project_root,
            entry_type=type,
            title=title,
            content=content,
            tags=list(tags),
            files_affected=list(files),
            llm_context=llm_context,
            related_entries=list(related_entries)
        )
        
        click.echo(f"✅ Entrada creada exitosamente con ID: {entry_id}")
        
        # Mostrar entrada creada
        memory_system = MemorySystem(project_root)
        entry = memory_system.get_entry(entry_id)
        if entry:
            click.echo("\n📝 Entrada creada:")
            click.echo(f"   ID: {entry.entry_id}")
            click.echo(f"   Tipo: {entry.entry_type}")
            click.echo(f"   Título: {entry.title}")
            click.echo(f"   Fecha: {entry.timestamp}")
            if entry.git_info:
                click.echo(f"   Git: {entry.git_info.get('current_commit', 'N/A')} ({entry.git_info.get('branch', 'N/A')})")
                if not entry.git_info.get('is_clean'):
                    click.echo(f"   ⚠️  Repositorio con cambios pendientes")
    
    except Exception as e:
        click.echo(f"❌ Error al crear entrada: {e}", err=True)
        if os.environ.get("MEMORIA_DEBUG"):
            click.echo(traceback.format_exc(), err=True)
        raise click.Abort()


@main.command(name="list")
@click.option('--limit', '-n', type=int, help='Número máximo de entradas a mostrar')
@click.option('--offset', '-o', type=int, default=0, help='Número de entradas a omitir desde el inicio (para paginación)')
@click.option('--type', '-t', help='Filtrar por tipo de entrada')
@click.option('--tags', '-g', multiple=True, help='Filtrar por etiquetas')
@click.option('--search', '-s', help='Buscar en título y contenido')
@click.option('--date-from', help='Fecha de inicio (YYYY-MM-DD)')
@click.option('--date-to', help='Fecha de fin (YYYY-MM-DD)')
@click.option('--show-git', is_flag=True, help='Mostrar información de Git')
@click.option('--stats', is_flag=True, help='Mostrar estadísticas en lugar de entradas')
@click.option('--interactive', '-i', is_flag=True, help='Modo interactivo')
@click.pass_context
def list_cmd(ctx, limit, offset, type, tags, search, date_from, date_to, show_git, stats, interactive):
    """Listar entradas del sistema de memoria."""
    project_root = ctx.obj['PROJECT_ROOT']
    
    if interactive:
        search_entries_interactive(project_root)
        return
    
    try:
        entries = list_entries(
            project_root=project_root,
            limit=limit,
            offset=offset,
            entry_type=type,
            tags=list(tags),
            search=search,
            date_from=date_from,
            date_to=date_to,
            show_git=show_git,
            stats=stats
        )
        
        if not stats:
            display_entries(entries, show_git=show_git, limit=limit, offset=offset)
    
    except Exception as e:
        click.echo(f"❌ Error al listar entradas: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('entry_id')
@click.option('--show-git', is_flag=True, help='Mostrar información de Git')
@click.pass_context
def show(ctx, entry_id, show_git):
    """Mostrar detalles completos de una entrada específica."""
    project_root = ctx.obj.get('PROJECT_ROOT') if ctx and ctx.obj else Path('.').resolve()
    
    try:
        memory_system = MemorySystem(project_root)
        entry = memory_system.get_entry(entry_id)
        
        if not entry:
            click.echo(f"❌ No se encontró la entrada con ID: {entry_id}", err=True)
            raise click.Abort()
        
        display_entry_details(entry, show_git=show_git)
    
    except Exception as e:
        click.echo(f"❌ Error al mostrar entrada: {e}", err=True)
        raise click.Abort()


@main.command()
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['markdown', 'json', 'text']), 
              default='markdown', help='Formato de salida')
@click.option('--include-git/--no-git', default=True, help='Incluir información de Git')
@click.option('--group-by', type=click.Choice(['type', 'date', 'tags']), 
              default='type', help='Agrupar entradas por')
@click.option('--limit', '-n', type=int, help='Número máximo de entradas a exportar')
@click.option('--summary', is_flag=True, help='Exportar solo resumen ejecutivo')
@click.option('--chunked', is_flag=True, help='Dividir exportación en múltiples archivos')
@click.option('--max-chars', type=int, help='Máximo de caracteres por archivo (aprox tokens*4)')
@click.option('--max-tokens', type=int, help='Máximo de tokens estimados por archivo')
@click.option('--type', '-t', 'entry_type', help='Filtrar por tipo de entrada')
@click.option('--tags', '-g', multiple=True, help='Filtrar por etiquetas')
@click.option('--search', '-s', help='Buscar en título, contenido y contexto')
@click.option('--date-from', help='Fecha de inicio (YYYY-MM-DD)')
@click.option('--date-to', help='Fecha de fin (YYYY-MM-DD)')
@click.pass_context
def export(ctx, output_format, include_git, group_by, limit, summary, entry_type, tags, search, date_from, date_to, chunked, max_chars, max_tokens):
    """Exportar entradas en formato optimizado para LLM."""
    project_root = ctx.obj['PROJECT_ROOT']
    
    try:
        exporter = LLMExporter(project_root)
        
        if summary:
            output_file = exporter.export_summary(output_format)
        else:
            output_file = exporter.export_for_llm(
                output_format=output_format,
                include_git=include_git,
                group_by=group_by,
                limit=limit,
                entry_type=entry_type,
                tags=list(tags),
                search=search,
                date_from=date_from,
                date_to=date_to,
                chunked=chunked,
                max_chars=max_chars,
                max_tokens=max_tokens
            )
        
        click.echo(f"✅ Exportación completada: {output_file}")
    
    except Exception as e:
        click.echo(f"❌ Error al exportar: {e}", err=True)
        raise click.Abort()


@main.command()
@click.option('--name', '-n', help='Nombre del proyecto')
@click.option('--description', '-d', help='Descripción del proyecto')
@click.pass_context
def init(ctx, name, description):
    """Inicializar el sistema de memoria en el proyecto actual."""
    project_root = ctx.obj.get('PROJECT_ROOT') if ctx and ctx.obj else Path('.').resolve()
    
    try:
        memory_system = MemorySystem(project_root)
        memory_system.initialize_project(project_name=name, project_description=description)
        
        click.echo(f"✅ Sistema de memoria inicializado en: {project_root}")
        click.echo("📁 Directorios creados: entries/, export/, config/")
        click.echo("📄 Archivos creados: config/config.json, .gitignore, MEMORIA.md")
        click.echo("\n🚀 Para crear tu primera entrada:")
        click.echo(f"   memoria create note 'Mi primera entrada' 'Contenido de la entrada'")
    
    except Exception as e:
        click.echo(f"❌ Error al inicializar: {e}", err=True)
        raise click.Abort()


@main.command()
@click.pass_context
def status(ctx):
    """Mostrar estado del sistema de memoria."""
    project_root = ctx.obj.get('PROJECT_ROOT') if ctx and ctx.obj else Path('.').resolve()
    
    try:
        memory_system = MemorySystem(project_root)
        stats = memory_system.get_statistics()
        
        click.echo(f"📊 Estado del Sistema de Memoria - {project_root.name}")
        click.echo("=" * 50)
        click.echo(f"Total de entradas: {stats.get('total_entries', 0)}")
        click.echo(f"Fecha de creación: {stats.get('created', 'N/A')[:10] if stats.get('created') else 'N/A'}")
        click.echo(f"Última actualización: {stats.get('last_updated', 'N/A')[:10] if stats.get('last_updated') else 'N/A'}")
        
        # Distribución por tipo
        by_type = stats.get('by_type', {})
        if by_type:
            click.echo("\nDistribución por tipo:")
            for entry_type, count in sorted(by_type.items()):
                percentage = (count / stats.get('total_entries', 1)) * 100
                click.echo(f"  {entry_type}: {count} ({percentage:.1f}%)")
        
        # Total de etiquetas únicas
        total_tags = stats.get('total_tags', [])
        click.echo(f"\nEtiquetas únicas: {len(total_tags)}")
        if total_tags:
            click.echo(f"Lista: {', '.join(sorted(total_tags))}")
        
        # Verificar integración Git
        git_integration = memory_system.git_integration
        if git_integration and git_integration.is_git_repository():
            git_info = git_integration.get_git_info()
            if git_info:
                click.echo(f"\n🔗 Integración Git:")
                click.echo(f"  Commit: {git_info.get('current_commit', 'N/A')}")
                click.echo(f"  Rama: {git_info.get('branch', 'N/A')}")
                click.echo(f"  Estado: {'Limpio' if git_info.get('is_clean') else 'Con cambios'}")
        else:
            click.echo("\n⚠️  No se detectó repositorio Git")
    
    except Exception as e:
        click.echo(f"❌ Error al obtener estado: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('entry_id')
@click.option('--title', help='Nuevo título')
@click.option('--content', help='Nuevo contenido')
@click.option('--tags', multiple=True, help='Nuevas etiquetas')
@click.option('--files', multiple=True, help='Nuevos archivos afectados')
@click.option('--llm-context', help='Nuevo contexto LLM')
@click.pass_context
def update(ctx, entry_id, title, content, tags, files, llm_context):
    """Actualizar una entrada existente."""
    project_root = ctx.obj.get('PROJECT_ROOT') if ctx and ctx.obj else Path('.').resolve()
    
    try:
        memory_system = MemorySystem(project_root)
        
        # Preparar campos a actualizar
        update_fields = {}
        if title:
            update_fields['title'] = title
        if content:
            update_fields['content'] = content
        if tags:
            update_fields['tags'] = list(tags)
        if files:
            update_fields['files_affected'] = list(files)
        if llm_context:
            update_fields['llm_context'] = llm_context
        
        if not update_fields:
            click.echo("❌ Debes especificar al menos un campo para actualizar", err=True)
            raise click.Abort()
        
        # Actualizar entrada
        success = memory_system.update_entry(entry_id, **update_fields)
        
        if success:
            click.echo(f"✅ Entrada {entry_id} actualizada exitosamente")
        else:
            click.echo(f"❌ No se pudo actualizar la entrada {entry_id}", err=True)
            raise click.Abort()
    
    except Exception as e:
        click.echo(f"❌ Error al actualizar entrada: {e}", err=True)
        raise click.Abort()


@main.command()
@click.argument('entry_id')
@click.option('--force', '-f', is_flag=True, help='Forzar eliminación sin confirmación')
@click.pass_context
def delete(ctx, entry_id, force):
    """Eliminar una entrada del sistema."""
    project_root = ctx.obj.get('PROJECT_ROOT') if ctx and ctx.obj else Path('.').resolve()
    
    try:
        memory_system = MemorySystem(project_root)
        entry = memory_system.get_entry(entry_id)
        
        if not entry:
            click.echo(f"❌ No se encontró la entrada con ID: {entry_id}", err=True)
            raise click.Abort()
        
        # Confirmar eliminación
        if not force:
            click.echo(f"¿Estás seguro de que quieres eliminar la entrada '{entry.title}'?")
            if not click.confirm("Esta acción no se puede deshacer"):
                click.echo("Operación cancelada")
                return
        
        # Eliminar entrada
        success = memory_system.delete_entry(entry_id)
        
        if success:
            click.echo(f"✅ Entrada {entry_id} eliminada exitosamente")
        else:
            click.echo(f"❌ No se pudo eliminar la entrada {entry_id}", err=True)
            raise click.Abort()
    
    except Exception as e:
        click.echo(f"❌ Error al eliminar entrada: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    main()
