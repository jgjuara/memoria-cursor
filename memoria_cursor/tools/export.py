"""
Herramienta para exportar entradas del sistema de memoria en formatos optimizados para LLM.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

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
                      limit: Optional[int] = None) -> str:
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
        
        # Obtener entradas
        entries = memory_system.list_entries(limit=limit)
        
        if not entries:
            raise ValueError("No hay entradas para exportar")
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"memory_export_{timestamp}"
        
        # Exportar según formato
        if output_format == "markdown":
            return self._export_markdown(entries, filename, include_git, group_by)
        elif output_format == "json":
            return self._export_json(entries, filename, include_git)
        elif output_format == "text":
            return self._export_text(entries, filename, include_git, group_by)
        else:
            raise ValueError(f"Formato no soportado: {output_format}")
    
    def _export_markdown(self, entries: List[Entry], 
                        filename: str, include_git: bool, group_by: str) -> str:
        """Exportar en formato Markdown."""
        output_file = self.export_dir / f"{filename}.md"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("# Memoria del Proyecto - Exportación para LLM\n\n")
            f.write(f"**Generado:** {datetime.now().isoformat()}\n")
            f.write(f"**Total de entradas:** {len(entries)}\n")
            f.write(f"**Proyecto:** {self.project_root.name}\n\n")
            
            # Agrupar entradas
            if group_by == "type":
                grouped = self._group_by_type(entries)
                for entry_type, type_entries in grouped.items():
                    f.write(f"## {entry_type.upper()}\n\n")
                    for entry in type_entries:
                        self._write_markdown_entry(f, entry, include_git)
                    f.write("\n")
            
            elif group_by == "date":
                grouped = self._group_by_date(entries)
                for date, date_entries in grouped.items():
                    f.write(f"## {date}\n\n")
                    for entry in date_entries:
                        self._write_markdown_entry(f, entry, include_git)
                    f.write("\n")
            
            else:  # Sin agrupar
                for entry in entries:
                    self._write_markdown_entry(f, entry, include_git)
                    f.write("\n")
        
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
    
    def _export_text(self, entries: List[Entry], filename: str, include_git: bool, group_by: str) -> str:
        """Exportar en formato texto plano."""
        output_file = self.export_dir / f"{filename}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            # Encabezado
            f.write("MEMORIA DEL PROYECTO - EXPORTACIÓN PARA LLM\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generado: {datetime.now().isoformat()}\n")
            f.write(f"Total de entradas: {len(entries)}\n")
            f.write(f"Proyecto: {self.project_root.name}\n\n")
            
            # Agrupar entradas
            if group_by == "type":
                grouped = self._group_by_type(entries)
                for entry_type, type_entries in grouped.items():
                    f.write(f"{entry_type.upper()}\n")
                    f.write("-" * len(entry_type) + "\n\n")
                    for entry in type_entries:
                        self._write_text_entry(f, entry, include_git)
                    f.write("\n")
            
            elif group_by == "date":
                grouped = self._group_by_date(entries)
                for date, date_entries in grouped.items():
                    f.write(f"{date}\n")
                    f.write("-" * len(date) + "\n\n")
                    for entry in date_entries:
                        self._write_text_entry(f, entry, include_git)
                    f.write("\n")
            
            else:  # Sin agrupar
                for entry in entries:
                    self._write_text_entry(f, entry, include_git)
                    f.write("\n")
        
        return str(output_file)
    
    def _write_markdown_entry(self, file, entry: Entry, include_git: bool):
        """Escribir entrada en formato Markdown."""
        # Encabezado de entrada
        file.write(f"### {entry.title}\n\n")
        
        # Metadatos
        file.write(f"**Tipo:** {entry.entry_type}\n")
        file.write(f"**ID:** {entry.entry_id}\n")
        file.write(f"**Fecha:** {entry.timestamp}\n")
        
        if entry.tags:
            file.write(f"**Etiquetas:** {', '.join(entry.tags)}\n")
        
        if entry.files_affected:
            file.write(f"**Archivos:** {', '.join(entry.files_affected)}\n")
        
        # Información de Git
        if include_git and entry.git_info:
            git_info = entry.git_info
            file.write(f"**Git:** {git_info.get('current_commit', 'N/A')} ")
            file.write(f"({git_info.get('branch', 'N/A')})")
            if not git_info.get('is_clean'):
                file.write(" ⚠️ Cambios pendientes")
            file.write("\n")
        
        file.write("\n")
        
        # Contenido
        file.write(f"{entry.content}\n\n")
        
        # Contexto LLM
        if entry.llm_context:
            file.write("> **Contexto LLM:** " + entry.llm_context + "\n\n")
        
        file.write("---\n\n")
    
    def _write_text_entry(self, file, entry: Entry, include_git: bool):
        """Escribir entrada en formato texto plano."""
        # Encabezado de entrada
        file.write(f"ENTRADA: {entry.title}\n")
        file.write("-" * (len(entry.title) + 9) + "\n\n")
        
        # Metadatos
        file.write(f"Tipo: {entry.entry_type}\n")
        file.write(f"ID: {entry.entry_id}\n")
        file.write(f"Fecha: {entry.timestamp}\n")
        
        if entry.tags:
            file.write(f"Etiquetas: {', '.join(entry.tags)}\n")
        
        if entry.files_affected:
            file.write(f"Archivos: {', '.join(entry.files_affected)}\n")
        
        # Información de Git
        if include_git and entry.git_info:
            git_info = entry.git_info
            file.write(f"Git: {git_info.get('current_commit', 'N/A')} ")
            file.write(f"({git_info.get('branch', 'N/A')})")
            if not git_info.get('is_clean'):
                file.write(" [CAMBIOS PENDIENTES]")
            file.write("\n")
        
        file.write("\n")
        
        # Contenido
        file.write(f"CONTENIDO:\n{entry.content}\n\n")
        
        # Contexto LLM
        if entry.llm_context:
            file.write(f"CONTEXTO LLM: {entry.llm_context}\n\n")
        
        file.write("=" * 60 + "\n\n")
    
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
