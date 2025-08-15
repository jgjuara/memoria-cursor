"""
Clase Entry para representar entradas del sistema de memoria.
"""

import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class Entry:
    """
    Representa una entrada en el sistema de memoria.
    
    Attributes:
        entry_type: Tipo de entrada (decision, change, context, bug, feature, note)
        title: Título descriptivo de la entrada
        content: Contenido principal de la entrada
        tags: Lista de etiquetas para categorización
        files_affected: Lista de archivos afectados
        llm_context: Contexto específico para agentes LLM
        git_info: Información de Git (commit, rama, estado)
        related_entries: Lista de IDs de entradas relacionadas para contexto
        timestamp: Fecha y hora de creación
        entry_id: Identificador único de la entrada
    """
    
    entry_type: str
    title: str
    content: str
    tags: List[str] = field(default_factory=list)
    files_affected: List[str] = field(default_factory=list)
    llm_context: Optional[str] = None
    git_info: Optional[Dict[str, Any]] = None
    related_entries: List[str] = field(default_factory=list)
    timestamp: Optional[str] = None
    entry_id: Optional[str] = None
    
    def __post_init__(self):
        """Inicializar valores por defecto después de la creación."""
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        
        if self.entry_id is None:
            self.entry_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generar ID único usando UUID."""
        return str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir entrada a diccionario."""
        return {
            "id": self.entry_id,
            "timestamp": self.timestamp,
            "type": self.entry_type,
            "title": self.title,
            "content": self.content,
            "tags": self.tags,
            "files_affected": self.files_affected,
            "llm_context": self.llm_context,
            "git_info": self.git_info,
            "related_entries": self.related_entries
        }
    
    def to_json(self) -> str:
        """Convertir entrada a JSON string."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entry':
        """Crear entrada desde diccionario."""
        return cls(
            entry_type=data.get("type", ""),
            title=data.get("title", ""),
            content=data.get("content", ""),
            tags=data.get("tags", []),
            files_affected=data.get("files_affected", []),
            llm_context=data.get("llm_context"),
            git_info=data.get("git_info"),
            related_entries=data.get("related_entries", []),
            timestamp=data.get("timestamp"),
            entry_id=data.get("id")
        )
    
    def add_tag(self, tag: str) -> None:
        """Agregar etiqueta a la entrada."""
        if tag not in self.tags:
            self.tags.append(tag)
    
    def remove_tag(self, tag: str) -> bool:
        """Remover etiqueta de la entrada."""
        try:
            self.tags.remove(tag)
            return True
        except ValueError:
            return False
    
    def add_file(self, file_path: str) -> None:
        """Agregar archivo afectado."""
        if file_path not in self.files_affected:
            self.files_affected.append(file_path)
    
    def remove_file(self, file_path: str) -> bool:
        """Remover archivo afectado."""
        try:
            self.files_affected.remove(file_path)
            return True
        except ValueError:
            return False
    
    def add_related_entry(self, entry_id: str) -> None:
        """Agregar entrada relacionada por ID."""
        if entry_id not in self.related_entries:
            self.related_entries.append(entry_id)
    
    def remove_related_entry(self, entry_id: str) -> bool:
        """Remover entrada relacionada por ID."""
        try:
            self.related_entries.remove(entry_id)
            return True
        except ValueError:
            return False
    
    def has_related_entries(self) -> bool:
        """Verificar si la entrada tiene entradas relacionadas."""
        return len(self.related_entries) > 0
    
    def update_content(self, new_content: str) -> None:
        """Actualizar contenido de la entrada."""
        self.content = new_content
        self.timestamp = datetime.now().isoformat()
    
    def has_tag(self, tag: str) -> bool:
        """Verificar si la entrada tiene una etiqueta específica."""
        return tag in self.tags
    
    def matches_search(self, search_term: str) -> bool:
        """Verificar si la entrada coincide con un término de búsqueda."""
        search_lower = search_term.lower()
        return (search_lower in self.title.lower() or 
                search_lower in self.content.lower() or
                any(search_lower in tag.lower() for tag in self.tags))
    
    def __str__(self) -> str:
        """Representación string de la entrada."""
        return f"[{self.entry_type.upper()}] {self.title} - {self.timestamp}"
    
    def __repr__(self) -> str:
        """Representación detallada de la entrada."""
        return f"Entry(type='{self.entry_type}', title='{self.title}', id='{self.entry_id}')"
