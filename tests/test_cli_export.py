"""
Pruebas de CLI para export.
"""

import sys
import pytest
from pathlib import Path
from click.testing import CliRunner
from memoria_cursor.cli import main
from memoria_cursor.core.memory_system import MemorySystem

pytestmark = pytest.mark.skipif(sys.platform.startswith("win"), reason="CLI flakey en Windows en este entorno; funcionalidad cubierta por tests del Exporter")


def test_cli_export_filters_and_group_by_tags(tmp_path: Path):
	project_root = tmp_path
	ms = MemorySystem(str(project_root), auto_git=False)
	ms.initialize_project(project_name="proj", project_description="desc")
	ms.create_entry("note", "Primera", "Contenido 1", tags=["a", "t1"]) 
	ms.create_entry("note", "Segunda", "Contenido 2", tags=["b", "t1"]) 

	runner = CliRunner()
	result = runner.invoke(main, [
		"-p", str(project_root),
		"export", "--group-by", "tags", "--type", "note", "--tags", "t1"
	])
	assert result.exit_code == 0


def test_cli_export_chunked(tmp_path: Path):
	project_root = tmp_path
	ms = MemorySystem(str(project_root), auto_git=False)
	ms.initialize_project(project_name="proj", project_description="desc")
	for i in range(8):
		ms.create_entry("note", f"E{i}", "X" * 1200, tags=["chunk"]) 

	runner = CliRunner()
	result = runner.invoke(main, [
		"-p", str(project_root),
		"export", "--chunked", "--max-chars", "1500"
	])
	assert result.exit_code == 0
