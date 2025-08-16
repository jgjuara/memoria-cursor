"""
Herramienta para exportar entradas del sistema de memoria en formatos optimizados para LLM.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

from ..core.memory_system import MemorySystem
from ..core.entry import Entry


class LLMExporter:
    """
    Clase para exportar entradas a formato optimizado para agentes LLM.
    
    Formatos soportados:
    - Markdown: Formato legible y estructurado
    - JSON: Formato estructurado para procesamiento automático
    - Text: Formato simple de texto plano
    """
    
    def __init__(self, project_root: str = "."):
        """
        Inicializar exportador.
        
        Args:
            project_root: Ruta raíz del proyecto
        """
        self.project_root = Path(project_root).resolve()
        self.export_dir = self.project_root / "export"
        self.export_dir.mkdir(exist_ok=True)
    
    def export_for_llm(self, 
                      output_format: str = "markdown",
                      include_git: bool = True,
                      group_by: str = "type",
                      limit: Optional[int] = None,
                      entry_type: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      search: Optional[str] = None,
                      date_from: Optional[str] = None,
                      date_to: Optional[str] = None,
                      chunked: bool = False,
                      max_chars: Optional[int] = None,
                      max_tokens: Optional[int] = None) -> str:
        """
        Exportar entradas en formato optimizado para LLM.
        
        Args:
            output_format: Formato de salida (markdown, json, text)
            include_git: Incluir información de Git
            group_by: Agrupar por (type, date, tags)
            limit: Número máximo de entradas a exportar
            
        Returns:
            Ruta del archivo exportado
            
        Raises:
            ValueError: Si el formato no es soportado
        """
        # Inicializar sistema de memoria
        memory_system = MemorySystem(self.project_root)
        
        # Obtener entradas con filtros
        entries = memory_system.list_entries(
            limit=limit,
            entry_type=entry_type,
            tags=tags,
            search=search,
            date_from=date_from,
            date_to=date_to,
        )
        
        if not entries:
            raise ValueError("No hay entradas para exportar")
        
        # Aplicar límite desde config si no se pasó por argumento
        if limit is None:
            try:
                max_entries = int(memory_system._get_config_value("export.max_entries_per_export", 0) or 0)
                if max_entries > 0:
                    entries = entries[-max_entries:]
            except Exception:
                pass

        # Calcular límites de chunking
        effective_max_chars = 0
        if max_tokens and max_tokens > 0:
            # Aproximación: 1 token ~ 4 chars (heurística)
            effective_max_chars = max(effective_max_chars, max_tokens * 4)
        if max_chars and max_chars > 0:
            effective_max_chars = max(effective_max_chars, max_chars)

        # Generar nombre de archivo base
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"memory_export_{timestamp}"
        
        # Exportar según formato
        if output_format == "markdown":
            return self._export_markdown(entries, filename, include_git, group_by, chunked, effective_max_chars)
        elif output_format == "json":
            return self._export_json(entries, filename, include_git)
        elif output_format == "text":
            return self._export_text(entries, filename, include_git, group_by, chunked, effective_max_chars)
        else:
            raise ValueError(f"Formato no soportado: {output_format}")

    def _export_markdown(self, entries: List[Entry], 
                        filename: str, include_git: bool, group_by: str,
                        chunked: bool, max_chars: int) -> str:
        """Exportar en formato Markdown."""
        content = self._build_markdown_content(entries, include_git, group_by)
        if chunked and max_chars and max_chars > 0:
            return self._write_chunked(filename, content, "md", max_chars)
        output_file = self.export_dir / f"{filename}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(output_file)
    
    def _export_json(self, entries: List[Entry], filename: str, include_git: bool) -> str:
        """Exportar en formato JSON."""
        output_file = self.export_dir / f"{filename}.json"
        
        # Preparar datos para exportación
        export_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "project": self.project_root.name,
                "total_entries": len(entries),
                "format": "json",
                "include_git": include_git
            },
            "entries": []
        }
        
        for entry in entries:
            entry_data = entry.to_dict()
            
            # Remover información de Git si no se incluye
            if not include_git and "git_info" in entry_data:
                del entry_data["git_info"]
            
            export_data["entries"].append(entry_data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(output_file)
    
    def _export_text(self, entries: List[Entry], filename: str, include_git: bool, group_by: str,
                     chunked: bool, max_chars: int) -> str:
        """Exportar en formato texto plano."""
        content = self._build_text_content(entries, include_git, group_by)
        if chunked and max_chars and max_chars > 0:
            return self._write_chunked(filename, content, "txt", max_chars)
        output_file = self.export_dir / f"{filename}.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return str(output_file)

    def _build_markdown_content(self, entries: List[Entry], include_git: bool, group_by: str) -> str:
        parts: List[str] = []
        parts.append("# Memoria del Proyecto - Exportación para LLM\n\n")
        parts.append(f"**Generado:** {datetime.now().isoformat()}\n")
        parts.append(f"**Total de entradas:** {len(entries)}\n")
        parts.append(f"**Proyecto:** {self.project_root.name}\n\n")

        if group_by == "type":
            grouped = self._group_by_type(entries)
            for entry_type, type_entries in grouped.items():
                parts.append(f"## {entry_type.upper()}\n\n")
                for entry in type_entries:
                    buffer = []
                    self._write_markdown_entry(buffer, entry, include_git, as_list=True)
                    parts.append(''.join(buffer))
                parts.append("\n")
        elif group_by == "date":
            grouped = self._group_by_date(entries)
            for date, date_entries in grouped.items():
                parts.append(f"## {date}\n\n")
                for entry in date_entries:
                    buffer = []
                    self._write_markdown_entry(buffer, entry, include_git, as_list=True)
                    parts.append(''.join(buffer))
                parts.append("\n")
        elif group_by == "tags":
            grouped = self._group_by_tags(entries)
            for tag, tag_entries in grouped.items():
                parts.append(f"## #{tag}\n\n")
                for entry in tag_entries:
                    buffer = []
                    self._write_markdown_entry(buffer, entry, include_git, as_list=True)
                    parts.append(''.join(buffer))
                parts.append("\n")
        else:
            for entry in entries:
                buffer = []
                self._write_markdown_entry(buffer, entry, include_git, as_list=True)
                parts.append(''.join(buffer))
                parts.append("\n")
        return ''.join(parts)

    def _build_text_content(self, entries: List[Entry], include_git: bool, group_by: str) -> str:
        parts: List[str] = []
        parts.append("MEMORIA DEL PROYECTO - EXPORTACIÓN PARA LLM\n")
        parts.append("=" * 60 + "\n\n")
        parts.append(f"Generado: {datetime.now().isoformat()}\n")
        parts.append(f"Total de entradas: {len(entries)}\n")
        parts.append(f"Proyecto: {self.project_root.name}\n\n")

        if group_by == "type":
            grouped = self._group_by_type(entries)
            for entry_type, type_entries in grouped.items():
                parts.append(f"{entry_type.upper()}\n")
                parts.append("-" * len(entry_type) + "\n\n")
                for entry in type_entries:
                    buffer: List[str] = []
                    self._write_text_entry(buffer, entry, include_git, as_list=True)
                    parts.append(''.join(buffer))
                parts.append("\n")
        elif group_by == "date":
            grouped = self._group_by_date(entries)
            for date, date_entries in grouped.items():
                parts.append(f"{date}\n")
                parts.append("-" * len(date) + "\n\n")
                for entry in date_entries:
                    buffer = []
                    self._write_text_entry(buffer, entry, include_git, as_list=True)
                    parts.append(''.join(buffer))
                parts.append("\n")
        elif group_by == "tags":
            grouped = self._group_by_tags(entries)
            for tag, tag_entries in grouped.items():
                parts.append(f"#{tag}\n")
                parts.append("-" * (len(tag) + 1) + "\n\n")
                for entry in tag_entries:
                    buffer = []
                    self._write_text_entry(buffer, entry, include_git, as_list=True)
                    parts.append(''.join(buffer))
                parts.append("\n")
        else:
            for entry in entries:
                buffer = []
                self._write_text_entry(buffer, entry, include_git, as_list=True)
                parts.append(''.join(buffer))
                parts.append("\n")
        return ''.join(parts)

    def _write_chunked(self, filename_base: str, content: str, ext: str, max_chars: int) -> str:
        """Escribir contenido en múltiples archivos respetando un máximo de caracteres.

        Intenta dividir en separadores amigables (líneas que empiezan por '### ', 'ENTRADA:' o '---').
        Retorna la ruta del primer archivo generado.
        """
        if max_chars <= 0 or len(content) <= max_chars:
            output_file = self.export_dir / f"{filename_base}.{ext}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            return str(output_file)

        parts: List[str] = []
        start = 0
        content_len = len(content)
        while start < content_len:
            end = min(start + max_chars, content_len)
            # Buscar separador hacia atrás para no cortar en medio de una entrada
            slice_chunk = content[start:end]
            sep_idx = max(
                slice_chunk.rfind("\n### "),
                slice_chunk.rfind("\nENTRADA:"),
                slice_chunk.rfind("\n---\n"),
            )
            if sep_idx <= 0 or end == content_len:
                cut = end
            else:
                cut = start + sep_idx
            parts.append(content[start:cut])
            start = cut
        # Escribir archivos
        first_path = None
        for i, part in enumerate(parts, start=1):
            output_file = self.export_dir / f"{filename_base}_part{i}.{ext}"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(part)
            if first_path is None:
                first_path = str(output_file)
        return first_path if first_path else str(self.export_dir / f"{filename_base}.{ext}")
    
    def _write_markdown_entry(self, file_or_list, entry: Entry, include_git: bool, as_list: bool = False):
        """Escribir entrada en formato Markdown."""
        writer = (lambda s: file_or_list.append(s)) if as_list else (lambda s: file_or_list.write(s))
        writer(f"### {entry.title}\n\n")
        writer(f"**Tipo:** {entry.entry_type}\n")
        writer(f"**ID:** {entry.entry_id}\n")
        writer(f"**Fecha:** {entry.timestamp}\n")
        if entry.tags:
            writer(f"**Etiquetas:** {', '.join(entry.tags)}\n")
        if entry.files_affected:
            writer(f"**Archivos:** {', '.join(entry.files_affected)}\n")
        if include_git and entry.git_info:
            git_info = entry.git_info
            writer(f"**Git:** {git_info.get('current_commit', 'N/A')} ")
            writer(f"({git_info.get('branch', 'N/A')})")
            if not git_info.get('is_clean'):
                writer(" ⚠️ Cambios pendientes")
            writer("\n")
        writer("\n")
        writer(f"{entry.content}\n\n")
        if entry.llm_context:
            writer("> **Contexto LLM:** " + entry.llm_context + "\n\n")
        writer("---\n\n")
    
    def _write_text_entry(self, file_or_list, entry: Entry, include_git: bool, as_list: bool = False):
        """Escribir entrada en formato texto plano."""
        writer = (lambda s: file_or_list.append(s)) if as_list else (lambda s: file_or_list.write(s))
        writer(f"ENTRADA: {entry.title}\n")
        writer("-" * (len(entry.title) + 9) + "\n\n")
        writer(f"Tipo: {entry.entry_type}\n")
        writer(f"ID: {entry.entry_id}\n")
        writer(f"Fecha: {entry.timestamp}\n")
        if entry.tags:
            writer(f"Etiquetas: {', '.join(entry.tags)}\n")
        if entry.files_affected:
            writer(f"Archivos: {', '.join(entry.files_affected)}\n")
        if include_git and entry.git_info:
            git_info = entry.git_info
            writer(f"Git: {git_info.get('current_commit', 'N/A')} ")
            writer(f"({git_info.get('branch', 'N/A')})")
            if not git_info.get('is_clean'):
                writer(" [CAMBIOS PENDIENTES]")
            writer("\n")
        writer("\n")
        writer(f"CONTENIDO:\n{entry.content}\n\n")
        if entry.llm_context:
            writer(f"CONTEXTO LLM: {entry.llm_context}\n\n")
        writer("=" * 60 + "\n\n")
    
    def _group_by_type(self, entries: List[Entry]) -> Dict[str, List[Entry]]:
        """Agrupar entradas por tipo."""
        grouped = {}
        for entry in entries:
            entry_type = entry.entry_type
            if entry_type not in grouped:
                grouped[entry_type] = []
            grouped[entry_type].append(entry)
        
        # Ordenar por tipo
        return dict(sorted(grouped.items()))
    
    def _group_by_date(self, entries: List[Entry]) -> Dict[str, List[Entry]]:
        """Agrupar entradas por fecha."""
        grouped = {}
        for entry in entries:
            try:
                dt = datetime.fromisoformat(entry.timestamp)
                date = dt.strftime("%Y-%m-%d")
            except ValueError:
                date = entry.timestamp[:10] if entry.timestamp else "unknown"
            
            if date not in grouped:
                grouped[date] = []
            grouped[date].append(entry)
        
        # Ordenar por fecha (más reciente primero)
        return dict(sorted(grouped.items(), reverse=True))
    
    def _group_by_tags(self, entries: List[Entry]) -> Dict[str, List[Entry]]:
        """Agrupar entradas por etiquetas."""
        grouped = {}
        for entry in entries:
            for tag in entry.tags:
                if tag not in grouped:
                    grouped[tag] = []
                grouped[tag].append(entry)
        
        # Ordenar por etiqueta
        return dict(sorted(grouped.items()))
    
    def export_summary(self, output_format: str = "markdown") -> str:
        """
        Exportar resumen ejecutivo de las entradas.
        
        Args:
            output_format: Formato de salida
            
        Returns:
            Ruta del archivo exportado
        """
        memory_system = MemorySystem(self.project_root)
        stats = memory_system.get_statistics()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"memory_summary_{timestamp}"
        
        if output_format == "markdown":
            return self._export_summary_markdown(stats, filename)
        elif output_format == "json":
            return self._export_summary_json(stats, filename)
        else:
            return self._export_summary_text(stats, filename)
    
    def _export_summary_markdown(self, stats: Dict[str, Any], filename: str) -> str:
        """Exportar resumen en formato Markdown."""
        output_file = self.export_dir / f"{filename}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# Resumen Ejecutivo - Sistema de Memoria\n\n")
            f.write(f"**Generado:** {datetime.now().isoformat()}\n")
            f.write(f"**Proyecto:** {self.project_root.name}\n\n")
            
            f.write(f"## Estadísticas Generales\n\n")
            f.write(f"- **Total de entradas:** {stats.get('total_entries', 0)}\n")
            f.write(f"- **Fecha de creación:** {stats.get('created', 'N/A')}\n")
            f.write(f"- **Última actualización:** {stats.get('last_updated', 'N/A')}\n\n")
            
            f.write(f"## Distribución por Tipo\n\n")
            by_type = stats.get('by_type', {})
            for entry_type, count in sorted(by_type.items()):
                percentage = (count / stats.get('total_entries', 1)) * 100
                f.write(f"- **{entry_type}:** {count} ({percentage:.1f}%)\n")
            
            f.write(f"\n## Etiquetas Únicas\n\n")
            total_tags = stats.get('total_tags', [])
            f.write(f"- **Total:** {len(total_tags)}\n")
            if total_tags:
                f.write(f"- **Lista:** {', '.join(sorted(total_tags))}\n")
        
        return str(output_file)
    
    def _export_summary_json(self, stats: Dict[str, Any], filename: str) -> str:
        """Exportar resumen en formato JSON."""
        output_file = self.export_dir / f"{filename}.json"
        
        export_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "project": self.project_root.name,
                "format": "summary_json"
            },
            "statistics": stats
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return str(output_file)
    
    def _export_summary_text(self, stats: Dict[str, Any], filename: str) -> str:
        """Exportar resumen en formato texto."""
        output_file = self.export_dir / f"{filename}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("RESUMEN EJECUTIVO - SISTEMA DE MEMORIA\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generado: {datetime.now().isoformat()}\n")
            f.write(f"Proyecto: {self.project_root.name}\n\n")
            
            f.write(f"ESTADÍSTICAS GENERALES\n")
            f.write("-" * 25 + "\n")
            f.write(f"Total de entradas: {stats.get('total_entries', 0)}\n")
            f.write(f"Fecha de creación: {stats.get('created', 'N/A')}\n")
            f.write(f"Última actualización: {stats.get('last_updated', 'N/A')}\n\n")
            
            f.write(f"DISTRIBUCIÓN POR TIPO\n")
            f.write("-" * 22 + "\n")
            by_type = stats.get('by_type', {})
            for entry_type, count in sorted(by_type.items()):
                percentage = (count / stats.get('total_entries', 1)) * 100
                f.write(f"{entry_type}: {count} ({percentage:.1f}%)\n")
            
            f.write(f"\nETIQUETAS ÚNICAS\n")
            f.write("-" * 15 + "\n")
            total_tags = stats.get('total_tags', [])
            f.write(f"Total: {len(total_tags)}\n")
            if total_tags:
                f.write(f"Lista: {', '.join(sorted(total_tags))}\n")
        
        return str(output_file)
