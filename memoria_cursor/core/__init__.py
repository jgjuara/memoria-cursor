"""
Módulo core del sistema de memoria.

Contiene las clases y funcionalidades principales del sistema.
"""

from .entry import Entry
from .memory_system import MemorySystem
from .git_integration import GitIntegration

__all__ = ["Entry", "MemorySystem", "GitIntegration"]
