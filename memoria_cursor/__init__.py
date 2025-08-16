"""
Sistema de Memoria para Agentes LLM

Una herramienta sencilla, liviana y portable para registrar información relevante 
del desarrollo de proyectos que puede alimentar las interacciones con agentes LLM 
(Cursor, Claude Code, etc.).

Características principales:
- Sistema de entradas JSON estructuradas
- Integración automática con Git
- Herramientas CLI para gestión
- Exportación optimizada para LLM
- Fácil integración en cualquier proyecto
"""

__version__ = "1.0.3"
__author__ = "Tu Nombre"
__email__ = "tu@email.com"

from .core.memory_system import MemorySystem
from .core.entry import Entry
from .core.git_integration import GitIntegration

__all__ = [
    "MemorySystem",
    "Entry", 
    "GitIntegration",
    "__version__",
    "__author__",
    "__email__",
]
