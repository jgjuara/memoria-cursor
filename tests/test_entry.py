"""
Pruebas para la clase Entry.
"""

import pytest
import uuid
from datetime import datetime
from memoria_cursor.core.entry import Entry


class TestEntry:
    """Pruebas para la clase Entry."""
    
    def test_entry_creation(self):
        """Probar creación básica de entrada."""
        entry = Entry(
            entry_type="note",
            title="Test Entry",
            content="Test content"
        )
        
        assert entry.entry_type == "note"
        assert entry.title == "Test Entry"
        assert entry.content == "Test content"
        assert entry.entry_id is not None
        assert entry.timestamp is not None
    
    def test_entry_with_optional_fields(self):
        """Probar creación de entrada con campos opcionales."""
        entry = Entry(
            entry_type="decision",
            title="Test Decision",
            content="Test decision content",
            tags=["test", "decision"],
            files_affected=["test.py"],
            llm_context="Test LLM context"
        )
        
        assert entry.tags == ["test", "decision"]
        assert entry.files_affected == ["test.py"]
        assert entry.llm_context == "Test LLM context"
    
    def test_entry_id_generation(self):
        """Probar generación automática de ID."""
        entry = Entry(
            entry_type="note",
            title="Test",
            content="Test"
        )
        
        # El ID debe ser una cadena no vacía
        assert isinstance(entry.entry_id, str)
        assert len(entry.entry_id) > 0
        
        # El ID debe ser un UUID válido
        assert len(entry.entry_id) == 36  # Formato UUID: 8-4-4-4-12
        assert entry.entry_id.count("-") == 4
        # Verificar que es un UUID válido
        uuid.UUID(entry.entry_id)
    
    def test_entry_to_dict(self):
        """Probar conversión a diccionario."""
        entry = Entry(
            entry_type="note",
            title="Test",
            content="Test content",
            tags=["test"]
        )
        
        entry_dict = entry.to_dict()
        
        assert isinstance(entry_dict, dict)
        assert entry_dict["type"] == "note"
        assert entry_dict["title"] == "Test"
        assert entry_dict["content"] == "Test content"
        assert entry_dict["tags"] == ["test"]
        assert "id" in entry_dict
        assert "timestamp" in entry_dict
    
    def test_entry_from_dict(self):
        """Probar creación desde diccionario."""
        test_uuid = "550e8400-e29b-41d4-a716-446655440000"
        entry_data = {
            "id": test_uuid,
            "timestamp": "2025-01-01T12:00:00",
            "type": "note",
            "title": "Test",
            "content": "Test content",
            "tags": ["test"],
            "files_affected": [],
            "llm_context": None
        }
        
        entry = Entry.from_dict(entry_data)
        
        assert entry.entry_id == test_uuid
        assert entry.timestamp == "2025-01-01T12:00:00"
        assert entry.entry_type == "note"
        assert entry.title == "Test"
        assert entry.content == "Test content"
        assert entry.tags == ["test"]
    
    def test_entry_tag_operations(self):
        """Probar operaciones con etiquetas."""
        entry = Entry(
            entry_type="note",
            title="Test",
            content="Test"
        )
        
        # Agregar etiquetas
        entry.add_tag("tag1")
        entry.add_tag("tag2")
        assert entry.tags == ["tag1", "tag2"]
        
        # No duplicar etiquetas
        entry.add_tag("tag1")
        assert entry.tags == ["tag1", "tag2"]
        
        # Remover etiquetas
        assert entry.remove_tag("tag1") is True
        assert entry.tags == ["tag2"]
        
        # Remover etiqueta inexistente
        assert entry.remove_tag("nonexistent") is False
    
    def test_entry_file_operations(self):
        """Probar operaciones con archivos afectados."""
        entry = Entry(
            entry_type="note",
            title="Test",
            content="Test"
        )
        
        # Agregar archivos
        entry.add_file("file1.py")
        entry.add_file("file2.py")
        assert entry.files_affected == ["file1.py", "file2.py"]
        
        # No duplicar archivos
        entry.add_file("file1.py")
        assert entry.files_affected == ["file1.py", "file2.py"]
        
        # Remover archivos
        assert entry.remove_file("file1.py") is True
        assert entry.files_affected == ["file2.py"]
    
    def test_entry_content_update(self):
        """Probar actualización de contenido."""
        entry = Entry(
            entry_type="note",
            title="Test",
            content="Original content"
        )
        
        original_timestamp = entry.timestamp
        
        # Actualizar contenido
        entry.update_content("Updated content")
        
        assert entry.content == "Updated content"
        assert entry.timestamp != original_timestamp  # Timestamp debe actualizarse
    
    def test_entry_search_matching(self):
        """Probar búsqueda en entrada."""
        entry = Entry(
            entry_type="note",
            title="Test Entry Title",
            content="This is test content",
            tags=["test", "example"]
        )
        
        # Búsqueda en título
        assert entry.matches_search("Title") is True
        assert entry.matches_search("entry") is True
        
        # Búsqueda en contenido
        assert entry.matches_search("test content") is True
        assert entry.matches_search("This is") is True
        
        # Búsqueda en etiquetas
        assert entry.matches_search("test") is True
        assert entry.matches_search("example") is True
        
        # Búsqueda que no coincide
        assert entry.matches_search("nonexistent") is False
    
    def test_entry_string_representation(self):
        """Probar representación string de la entrada."""
        entry = Entry(
            entry_type="note",
            title="Test Entry",
            content="Test content"
        )
        
        str_repr = str(entry)
        assert "[NOTE]" in str_repr
        assert "Test Entry" in str_repr
        assert entry.timestamp in str_repr
    
    def test_entry_repr_representation(self):
        """Probar representación repr de la entrada."""
        entry = Entry(
            entry_type="note",
            title="Test Entry",
            content="Test content"
        )
        
        repr_str = repr(entry)
        assert "Entry" in repr_str
        assert "note" in repr_str
        assert "Test Entry" in repr_str
        assert entry.entry_id in repr_str


def test_entry_related_entries():
    """Test related entries functionality."""
    entry = Entry(
        entry_type="change",
        title="Test Entry",
        content="Test content",
        related_entries=["2025-08-08-001", "2025-08-08-002"]
    )
    
    assert len(entry.related_entries) == 2
    assert "2025-08-08-001" in entry.related_entries
    assert "2025-08-08-002" in entry.related_entries
    assert entry.has_related_entries() is True


def test_entry_add_remove_related_entries():
    """Test adding and removing related entries."""
    entry = Entry(
        entry_type="decision",
        title="Test Decision",
        content="Test decision content"
    )
    
    # Initially no related entries
    assert len(entry.related_entries) == 0
    assert entry.has_related_entries() is False
    
    # Add related entry
    entry.add_related_entry("2025-08-08-001")
    assert len(entry.related_entries) == 1
    assert "2025-08-08-001" in entry.related_entries
    assert entry.has_related_entries() is True
    
    # Add another related entry
    entry.add_related_entry("2025-08-08-002")
    assert len(entry.related_entries) == 2
    
    # Remove related entry
    assert entry.remove_related_entry("2025-08-08-001") is True
    assert len(entry.related_entries) == 1
    assert "2025-08-08-001" not in entry.related_entries
    assert "2025-08-08-002" in entry.related_entries
    
    # Try to remove non-existent entry
    assert entry.remove_related_entry("2025-08-08-999") is False


def test_entry_related_entries_serialization():
    """Test that related entries are properly serialized and deserialized."""
    original_entry = Entry(
        entry_type="feature",
        title="Test Feature",
        content="Test feature content",
        related_entries=["2025-08-08-001", "2025-08-08-003"]
    )
    
    # Convert to dict and back
    entry_dict = original_entry.to_dict()
    restored_entry = Entry.from_dict(entry_dict)
    
    # Verify related entries are preserved
    assert restored_entry.related_entries == original_entry.related_entries
    assert len(restored_entry.related_entries) == 2
    assert "2025-08-08-001" in restored_entry.related_entries
    assert "2025-08-08-003" in restored_entry.related_entries


def test_entry_related_entries_empty():
    """Test that empty related entries list is handled correctly."""
    entry = Entry(
        entry_type="note",
        title="Test Note",
        content="Test note content"
    )
    
    # Should have empty list by default
    assert entry.related_entries == []
    assert entry.has_related_entries() is False
    
    # Serialization should handle empty list
    entry_dict = entry.to_dict()
    assert "related_entries" in entry_dict
    assert entry_dict["related_entries"] == []
    
    # Deserialization should handle empty list
    restored_entry = Entry.from_dict(entry_dict)
    assert restored_entry.related_entries == []
    assert restored_entry.has_related_entries() is False
