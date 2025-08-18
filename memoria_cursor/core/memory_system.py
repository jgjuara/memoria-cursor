"""
Sistema principal de memoria que orquesta todas las funcionalidades.
"""

import json
import os
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from jsonschema import validate, ValidationError

from .entry import Entry
from .git_integration import GitIntegration


class MemorySystem:
    """
    Sistema principal de memoria que gestiona entradas, almacenamiento y operaciones.
    
    Funcionalidades:
    - Crear, leer, actualizar y eliminar entradas
    - Búsqueda y filtrado avanzado
    - Validación de esquemas JSON
    - Integración automática con Git
    - Exportación para agentes LLM
    """
    
    def __init__(self, project_root: str = ".", auto_git: bool = True):
        """
        Inicializar sistema de memoria.
        
        Args:
            project_root: Ruta raíz del proyecto
            auto_git: Habilitar integración automática con Git
        """
        self.project_root = Path(project_root).resolve()
        self.auto_git = auto_git
        
        # Directorios del sistema
        self.entries_dir = self.project_root / "entries"
        self.export_dir = self.project_root / "export"
        self.config_dir = self.project_root / "config"
        
        # Archivos del sistema
        self.entries_file = self.entries_dir / "entries.json"
        self.schema_file = self.config_dir / "schema.json"
        self.config_file = self.config_dir / "config.json"
        
        # Inicializar directorios y archivos
        self._initialize_system()
        
        # Integración con Git
        self.git_integration = GitIntegration(self.project_root) if auto_git else None
    
    def _load_schema(self) -> Optional[Dict[str, Any]]:
        """Cargar el esquema JSON para validar entradas.

        Prioriza el archivo del proyecto en `config/schema.json`. Si no existe,
        carga el esquema embebido en el paquete `memoria_cursor.config.schema.json`.
        """
        # Intentar cargar desde el proyecto
        try:
            if self.schema_file.exists():
                with open(self.schema_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass

        # Fallback: cargar esquema incluido en el paquete
        try:
            schema_text = resources.read_text('memoria_cursor.config', 'schema.json')
            return json.loads(schema_text)
        except Exception:
            return None

    def _validate_entry(self, entry: Entry) -> None:
        """Validar una entrada contra el esquema JSON si está disponible.

        Levanta ValueError con un mensaje claro si la validación falla.
        """
        schema = self._load_schema()
        if not schema:
            return  # Sin esquema, no validar

        try:
            validate(instance=entry.to_dict(), schema=schema)
        except ValidationError as exc:
            raise ValueError(f"Entrada inválida según schema.json: {exc.message}") from exc

    def _initialize_system(self) -> None:
        """Inicializar directorios y archivos del sistema."""
        # Crear directorios si no existen
        self.entries_dir.mkdir(parents=True, exist_ok=True)
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar archivo de entradas si no existe
        if not self.entries_file.exists():
            self._initialize_entries_file()
        
        # Inicializar archivo de configuración si no existe
        if not self.config_file.exists():
            self._initialize_config_file()
    
    def _initialize_entries_file(self) -> None:
        """Inicializar archivo de entradas con estructura básica."""
        initial_data = {
            "metadata": {
                "created": datetime.now(timezone.utc).isoformat(),
                "version": __import__('memoria_cursor').__version__,
                "total_entries": 0,
                "last_updated": datetime.now(timezone.utc).isoformat()
            },
            "entries": []
        }
        self._save_entries(initial_data)
    
    def _initialize_config_file(self) -> None:
        """Inicializar archivo de configuración por defecto."""
        default_config = {
            "project": {
                "name": self.project_root.name,
                "description": f"Proyecto {self.project_root.name}",
                "version": __import__('memoria_cursor').__version__
            },
            "system": {
                "auto_git": self.auto_git,
                "default_entry_type": "note",
                "max_content_length": 10000,
                "backup_enabled": True
            },
            "export": {
                "default_format": "markdown",
                "include_git_info": True,
                "group_by": "type"
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    def _load_entries(self) -> Dict[str, Any]:
        """Cargar entradas desde el archivo JSON."""
        try:
            with open(self.entries_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Asegurar estructura mínima válida
                if not isinstance(data, dict):
                    return {
                        "metadata": {
                            "created": datetime.now(timezone.utc).isoformat(),
                            "version": __import__('memoria_cursor').__version__,
                            "total_entries": 0,
                            "last_updated": datetime.now(timezone.utc).isoformat(),
                        },
                        "entries": [],
                    }
                if not isinstance(data.get("entries"), list):
                    data["entries"] = []
                if not isinstance(data.get("metadata"), dict):
                    data["metadata"] = {
                        "created": datetime.now(timezone.utc).isoformat(),
                        "version": __import__('memoria_cursor').__version__,
                        "total_entries": len(data["entries"]),
                        "last_updated": datetime.now(timezone.utc).isoformat(),
                    }
                else:
                    md = data["metadata"]
                    md.setdefault("created", datetime.now(timezone.utc).isoformat())
                    md.setdefault("version", __import__('memoria_cursor').__version__)
                    md.setdefault("total_entries", len(data["entries"]))
                    md.setdefault("last_updated", datetime.now(timezone.utc).isoformat())
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            # Si hay error, reinicializar el archivo
            self._initialize_entries_file()
            return self._load_entries()
    
    def _save_entries(self, data: Dict[str, Any]) -> None:
        """Guardar entradas en el archivo JSON."""
        # Crear backup si está habilitado
        if self._get_config_value("system.backup_enabled", True):
            self._create_backup()
        
        # Normalizar estructura antes de guardar
        if not isinstance(data, dict):
            data = {"metadata": {}, "entries": []}
        if not isinstance(data.get("entries"), list):
            data["entries"] = []
        if not isinstance(data.get("metadata"), dict):
            data["metadata"] = {}
        # Asegurar campos mínimos en metadata
        data["metadata"].setdefault("created", datetime.now(timezone.utc).isoformat())
        data["metadata"].setdefault("version", __import__('memoria_cursor').__version__)
        data["metadata"].setdefault("total_entries", len(data["entries"]))
        data["metadata"].setdefault("last_updated", datetime.now(timezone.utc).isoformat())

        with open(self.entries_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _create_backup(self) -> None:
        """Crear backup del archivo de entradas."""
        if self.entries_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.entries_dir / f"entries_backup_{timestamp}.json"
            
            try:
                with open(self.entries_file, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
            except Exception:
                pass  # Silenciar errores de backup
    
    def _get_config_value(self, key_path: str, default: Any = None) -> Any:
        """Obtener valor de configuración usando notación de punto."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

            value: Any = config
            for key in key_path.split('.'):
                if not isinstance(value, dict):
                    return default
                if key not in value:
                    return default
                value = value[key]
            return value
        except Exception:
            return default
    
    def create_entry(self, 
                    entry_type: str,
                    title: str,
                    content: str,
                    tags: Optional[List[str]] = None,
                    files_affected: Optional[List[str]] = None,
                    llm_context: Optional[str] = None,
                    related_entries: Optional[List[str]] = None) -> str:
        """
        Crear una nueva entrada en el sistema de memoria.
        
        Args:
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
            ValueError: Si el tipo de entrada es inválido
        """
        # Validar tipo de entrada
        valid_types = ["decision", "change", "context", "bug", "feature", "note"]
        if entry_type not in valid_types:
            raise ValueError(f"Tipo de entrada inválido. Debe ser uno de: {valid_types}")
        
        # Enforce límites desde config
        max_len = int(self._get_config_value("system.max_content_length", 10000) or 10000)
        if len(content) > max_len:
            raise ValueError(f"El contenido supera el máximo permitido ({max_len} caracteres)")
        if llm_context and len(llm_context) > max_len:
            raise ValueError(f"El llm_context supera el máximo permitido ({max_len} caracteres)")

        # Crear entrada
        entry = Entry(
            entry_type=entry_type,
            title=title,
            content=content,
            tags=tags or [],
            files_affected=files_affected or [],
            llm_context=llm_context,
            related_entries=related_entries or []
        )
        
        # Agregar información de Git si está disponible
        if self.auto_git and self.git_integration:
            git_info = self.git_integration.get_git_info()
            if git_info:
                entry.git_info = git_info
        
        # Validar contra schema si está disponible
        self._validate_entry(entry)

        # Cargar datos existentes
        data = self._load_entries()
        # Asegurar estructura mínima antes de modificar
        if not isinstance(data.get("entries"), list):
            data["entries"] = []
        if not isinstance(data.get("metadata"), dict):
            data["metadata"] = {
                "created": datetime.now(timezone.utc).isoformat(),
                "version": __import__('memoria_cursor').__version__,
                "total_entries": 0,
                "last_updated": datetime.now(timezone.utc).isoformat(),
            }
        
        # Agregar nueva entrada
        data["entries"].append(entry.to_dict())
        data["metadata"]["total_entries"] = len(data["entries"])
        data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        
        # Guardar datos
        self._save_entries(data)
        
        return entry.entry_id
    
    def get_entry(self, entry_id: str) -> Optional[Entry]:
        """
        Obtener una entrada específica por ID.
        
        Args:
            entry_id: ID de la entrada a buscar
            
        Returns:
            Objeto Entry o None si no se encuentra
        """
        data = self._load_entries()
        entries = data.get("entries", [])
        
        for entry_data in entries:
            if entry_data.get("id") == entry_id:
                return Entry.from_dict(entry_data)
        
        return None
    
    def list_entries(self,
                    limit: Optional[int] = None,
                    entry_type: Optional[str] = None,
                    tags: Optional[List[str]] = None,
                    search: Optional[str] = None,
                    date_from: Optional[str] = None,
                    date_to: Optional[str] = None) -> List[Entry]:
        """
        Listar entradas con filtros opcionales.
        
        Args:
            limit: Número máximo de entradas a retornar
            entry_type: Filtrar por tipo de entrada
            tags: Filtrar por etiquetas
            search: Buscar en título y contenido
            date_from: Fecha de inicio (YYYY-MM-DD)
            date_to: Fecha de fin (YYYY-MM-DD)
            
        Returns:
            Lista de entradas filtradas
        """
        data = self._load_entries()
        entries_data = data.get("entries", [])
        
        # Convertir a objetos Entry
        entries = [Entry.from_dict(entry_data) for entry_data in entries_data]
        
        # Aplicar filtros
        filtered_entries = entries
        
        # Filtrar por tipo
        if entry_type:
            filtered_entries = [
                entry for entry in filtered_entries
                if entry.entry_type == entry_type
            ]
        
        # Filtrar por etiquetas
        if tags:
            filtered_entries = [
                entry for entry in filtered_entries
                if any(tag in entry.tags for tag in tags)
            ]
        
        # Buscar en título y contenido
        if search:
            filtered_entries = [
                entry for entry in filtered_entries
                if entry.matches_search(search)
            ]
        
        # Filtrar por fecha
        if date_from or date_to:
            filtered_entries = self._filter_by_date(filtered_entries, date_from, date_to)
        
        # Aplicar límite
        if limit:
            filtered_entries = filtered_entries[-limit:]
        
        return filtered_entries
    
    def _filter_by_date(self, entries: List[Entry], 
                        date_from: Optional[str], 
                        date_to: Optional[str]) -> List[Entry]:
        """Filtrar entradas por rango de fechas."""
        filtered = entries
        
        if date_from:
            try:
                date_from_dt = datetime.fromisoformat(date_from + "T00:00:00")
                filtered = [
                    entry for entry in filtered
                    if datetime.fromisoformat(entry.timestamp) >= date_from_dt
                ]
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to_dt = datetime.fromisoformat(date_to + "T23:59:59")
                filtered = [
                    entry for entry in filtered
                    if datetime.fromisoformat(entry.timestamp) <= date_to_dt
                ]
            except ValueError:
                pass
        
        return filtered
    
    def update_entry(self, entry_id: str, **kwargs) -> bool:
        """
        Actualizar una entrada existente.
        
        Args:
            entry_id: ID de la entrada a actualizar
            **kwargs: Campos a actualizar
            
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        entry = self.get_entry(entry_id)
        if not entry:
            return False
        
        # Actualizar campos permitidos
        allowed_fields = ['title', 'content', 'tags', 'files_affected', 'llm_context']
        
        for field, value in kwargs.items():
            if field in allowed_fields and hasattr(entry, field):
                setattr(entry, field, value)
        
        # Actualizar timestamp
        entry.timestamp = datetime.now(timezone.utc).isoformat()
        
        # Validar contra schema si está disponible
        self._validate_entry(entry)

        # Guardar cambios
        data = self._load_entries()
        entries = data.get("entries", [])
        
        for i, entry_data in enumerate(entries):
            if entry_data.get("id") == entry_id:
                entries[i] = entry.to_dict()
                data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
                self._save_entries(data)
                return True
        
        return False
    
    def delete_entry(self, entry_id: str) -> bool:
        """
        Eliminar una entrada del sistema.
        
        Args:
            entry_id: ID de la entrada a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        data = self._load_entries()
        entries = data.get("entries", [])
        
        for i, entry_data in enumerate(entries):
            if entry_data.get("id") == entry_id:
                del entries[i]
                data["metadata"]["total_entries"] = len(entries)
                data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
                self._save_entries(data)
                return True
        
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtener estadísticas del sistema de memoria.
        
        Returns:
            Diccionario con estadísticas del sistema
        """
        data = self._load_entries()
        entries = data.get("entries", [])
        
        stats = {
            "total_entries": len(entries),
            "by_type": {},
            "by_date": {},
            "total_tags": set(),
            "created": data.get("metadata", {}).get("created"),
            "last_updated": data.get("metadata", {}).get("last_updated")
        }
        
        # Estadísticas por tipo
        for entry in entries:
            entry_type = entry.get("type", "unknown")
            stats["by_type"][entry_type] = stats["by_type"].get(entry_type, 0) + 1
            
            # Estadísticas por fecha
            timestamp = entry.get("timestamp", "")
            if timestamp:
                date = timestamp[:10]  # YYYY-MM-DD
                stats["by_date"][date] = stats["by_date"].get(date, 0) + 1
            
            # Total de etiquetas únicas
            tags = entry.get("tags", [])
            stats["total_tags"].update(tags)
        
        # Convertir set a lista para serialización JSON
        stats["total_tags"] = list(stats["total_tags"])
        
        return stats
    
    def export_entries(self, 
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
        """
        from ..tools.export import LLMExporter
        
        exporter = LLMExporter(self.project_root)
        return exporter.export_for_llm(output_format, include_git, group_by, limit)
    
    def initialize_project(self, project_name: Optional[str] = None, 
                          project_description: Optional[str] = None) -> None:
        """
        Inicializar el sistema de memoria en el proyecto actual.
        
        Args:
            project_name: Nombre del proyecto
            project_description: Descripción del proyecto
        """
        # Actualizar configuración del proyecto
        if project_name or project_description:
            self._update_project_config(project_name, project_description)
        
        # Crear archivo .gitignore si no existe
        self._create_gitignore()
        
        # Crear documentación del proyecto
        self._create_project_docs()
    
    def _update_project_config(self, project_name: Optional[str], 
                              project_description: Optional[str]) -> None:
        """Actualizar configuración del proyecto."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if project_name:
                config["project"]["name"] = project_name
            
            if project_description:
                config["project"]["description"] = project_description
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
                
        except Exception:
            pass
    
    def _create_gitignore(self) -> None:
        """Crear o actualizar archivo .gitignore."""
        gitignore_file = self.project_root / ".gitignore"
        
        memoria_entries = [
            "",
            "# Sistema de Memoria",
            "entries/",
            "export/",
            "config/install.json",
            ""
        ]
        
        if gitignore_file.exists():
            with open(gitignore_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "Sistema de Memoria" not in content:
                with open(gitignore_file, 'a', encoding='utf-8') as f:
                    f.write('\n'.join(memoria_entries))
        else:
            with open(gitignore_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(memoria_entries))
    
    def _create_project_docs(self) -> None:
        """Crear documentación específica del proyecto."""
        docs_content = f"""# Sistema de Memoria - {self.project_root.name}

## Descripción
Este proyecto utiliza el sistema de memoria para registrar información relevante del desarrollo que puede alimentar las interacciones con agentes LLM.

## Estructura
```
{self.project_root.name}/
├── entries/           # Entradas de memoria
├── export/            # Exportaciones para LLM
├── config/            # Configuración del sistema
└── .gitignore         # Configurado automáticamente
```

## Uso Rápido
1. Crear una entrada: `memoria create note "Mi primera entrada" "Contenido de la entrada"`
2. Listar entradas: `memoria list`
3. Exportar para LLM: `memoria export`

## Más Información
Ver documentación completa en: https://github.com/jgjuara/memoria-cursor
"""
        
        docs_file = self.project_root / "MEMORIA.md"
        with open(docs_file, 'w', encoding='utf-8') as f:
            f.write(docs_content)
