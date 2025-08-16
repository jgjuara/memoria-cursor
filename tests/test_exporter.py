"""
Pruebas del exportador LLM.
"""

from pathlib import Path
from memoria_cursor.core.memory_system import MemorySystem
from memoria_cursor.tools.export import LLMExporter


def test_export_group_by_tags_markdown(tmp_path: Path):
    project_root = tmp_path
    ms = MemorySystem(str(project_root), auto_git=False)
    ms.initialize_project(project_name="test-proj", project_description="test")

    # Crear entradas con tags
    ms.create_entry("note", "Primera", "Contenido 1", tags=["a", "common"])
    ms.create_entry("note", "Segunda", "Contenido 2", tags=["b", "common"])

    exporter = LLMExporter(str(project_root))
    output = exporter.export_for_llm(output_format="markdown", group_by="tags")

    out_path = Path(output)
    assert out_path.exists()
    text = out_path.read_text(encoding="utf-8")
    # Debe contener encabezados de tags y títulos
    assert "## #a" in text or "#a\n" in text
    assert "Primera" in text
    assert "Segunda" in text


def test_export_chunking(tmp_path: Path):
    project_root = tmp_path
    ms = MemorySystem(str(project_root), auto_git=False)
    ms.initialize_project(project_name="test-proj", project_description="test")

    # Crear varias entradas para forzar chunking
    long_content = "X" * 1000
    for i in range(10):
        ms.create_entry("note", f"Entrada {i}", long_content, tags=["chunk"])

    exporter = LLMExporter(str(project_root))
    output = exporter.export_for_llm(
        output_format="markdown",
        group_by="type",
        chunked=True,
        max_chars=1500,  # Forzar múltiples partes
    )

    first = Path(output)
    assert first.exists()
    # Debe existir al menos la parte 1
    assert first.name.endswith(".md")

