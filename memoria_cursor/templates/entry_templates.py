"""
Plantillas para diferentes tipos de entradas del sistema de memoria.
"""

from typing import Dict, Any


class EntryTemplates:
    """Plantillas predefinidas para diferentes tipos de entradas."""
    
    @staticmethod
    def get_template(entry_type: str) -> Dict[str, Any]:
        """
        Obtener plantilla para un tipo de entrada específico.
        
        Args:
            entry_type: Tipo de entrada
            
        Returns:
            Plantilla con campos y descripciones
        """
        templates = {
            "decision": {
                "title": "Título de la decisión",
                "content": "Descripción de la decisión tomada, alternativas consideradas y justificación.",
                "tags": ["decision", "arquitectura"],
                "llm_context": "Contexto para agentes LLM sobre esta decisión de diseño.",
                "description": "Decisiones de arquitectura y diseño del proyecto"
            },
            "change": {
                "title": "Descripción del cambio",
                "content": "Detalles del cambio implementado, archivos modificados y razones.",
                "tags": ["change", "refactor"],
                "llm_context": "Información para agentes LLM sobre este cambio en el código.",
                "description": "Cambios importantes en el código o estructura"
            },
            "context": {
                "title": "Título del contexto",
                "content": "Información de contexto relevante para entender el proyecto.",
                "tags": ["context", "background"],
                "llm_context": "Contexto histórico y de fondo para agentes LLM.",
                "description": "Información de contexto del proyecto"
            },
            "bug": {
                "title": "Descripción del bug",
                "content": "Detalles del problema encontrado, pasos para reproducir y solución.",
                "tags": ["bug", "issue"],
                "llm_context": "Información para agentes LLM sobre este problema y su resolución.",
                "description": "Problemas y bugs encontrados"
            },
            "feature": {
                "title": "Nombre de la funcionalidad",
                "content": "Descripción de la nueva funcionalidad implementada y su propósito.",
                "tags": ["feature", "enhancement"],
                "llm_context": "Contexto para agentes LLM sobre esta nueva funcionalidad.",
                "description": "Nuevas funcionalidades implementadas"
            },
            "note": {
                "title": "Título de la nota",
                "content": "Contenido de la nota o observación general.",
                "tags": ["note", "general"],
                "llm_context": "Información general para agentes LLM.",
                "description": "Notas generales y observaciones"
            }
        }
        
        return templates.get(entry_type, templates["note"])
    
    @staticmethod
    def get_all_templates() -> Dict[str, Dict[str, Any]]:
        """
        Obtener todas las plantillas disponibles.
        
        Returns:
            Diccionario con todas las plantillas
        """
        return {
            "decision": EntryTemplates.get_template("decision"),
            "change": EntryTemplates.get_template("change"),
            "context": EntryTemplates.get_template("context"),
            "bug": EntryTemplates.get_template("bug"),
            "feature": EntryTemplates.get_template("feature"),
            "note": EntryTemplates.get_template("note")
        }
    
    @staticmethod
    def get_template_suggestions(entry_type: str) -> Dict[str, str]:
        """
        Obtener sugerencias de etiquetas para un tipo de entrada.
        
        Args:
            entry_type: Tipo de entrada
            
        Returns:
            Diccionario con sugerencias de etiquetas
        """
        suggestions = {
            "decision": {
                "arquitectura": "Decisiones de arquitectura del sistema",
                "tecnologia": "Elección de tecnologías",
                "diseño": "Patrones de diseño",
                "escalabilidad": "Consideraciones de escalabilidad",
                "seguridad": "Decisiones de seguridad"
            },
            "change": {
                "refactor": "Refactorización de código",
                "optimizacion": "Optimizaciones de rendimiento",
                "mantenimiento": "Cambios de mantenimiento",
                "bugfix": "Corrección de bugs",
                "feature": "Nuevas funcionalidades"
            },
            "context": {
                "background": "Información de fondo",
                "requerimientos": "Requerimientos del proyecto",
                "stakeholders": "Interesados del proyecto",
                "restricciones": "Restricciones técnicas o de negocio",
                "historia": "Historia del proyecto"
            },
            "bug": {
                "crash": "Errores que causan cierre del programa",
                "performance": "Problemas de rendimiento",
                "ui": "Problemas de interfaz de usuario",
                "data": "Problemas con datos",
                "security": "Vulnerabilidades de seguridad"
            },
            "feature": {
                "frontend": "Funcionalidades de interfaz",
                "backend": "Funcionalidades del servidor",
                "api": "Nuevas APIs",
                "database": "Cambios en base de datos",
                "integration": "Integraciones con otros sistemas"
            },
            "note": {
                "general": "Notas generales",
                "meeting": "Notas de reuniones",
                "research": "Resultados de investigación",
                "learning": "Aprendizajes del proyecto",
                "todo": "Tareas pendientes"
            }
        }
        
        return suggestions.get(entry_type, {})
    
    @staticmethod
    def get_quick_template(entry_type: str) -> str:
        """
        Obtener plantilla rápida para crear una entrada.
        
        Args:
            entry_type: Tipo de entrada
            
        Returns:
            Plantilla de texto para la entrada
        """
        templates = {
            "decision": """# Decisión: [Título de la decisión]

## Contexto
[Describir el contexto que llevó a esta decisión]

## Alternativas Consideradas
- [Alternativa 1]
- [Alternativa 2]
- [Alternativa 3]

## Decisión Tomada
[Describir la decisión final]

## Justificación
[Explicar por qué se tomó esta decisión]

## Impacto
[Describir el impacto en el proyecto]""",
            
            "change": """# Cambio: [Descripción del cambio]

## Archivos Modificados
- [Archivo 1]
- [Archivo 2]

## Razones del Cambio
[Explicar por qué se realizó este cambio]

## Implementación
[Describir cómo se implementó el cambio]

## Resultado
[Describir el resultado del cambio]""",
            
            "context": """# Contexto: [Título del contexto]

## Información de Fondo
[Describir el contexto histórico o de fondo]

## Relevancia
[Explicar por qué es importante para el proyecto]

## Referencias
[Incluir referencias o fuentes relevantes]""",
            
            "bug": """# Bug: [Descripción del problema]

## Pasos para Reproducir
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

## Comportamiento Esperado
[Describir qué debería suceder]

## Comportamiento Actual
[Describir qué está sucediendo]

## Solución Implementada
[Describir cómo se resolvió el problema]""",
            
            "feature": """# Funcionalidad: [Nombre de la funcionalidad]

## Propósito
[Explicar para qué sirve esta funcionalidad]

## Implementación
[Describir cómo se implementó]

## Archivos Afectados
- [Archivo 1]
- [Archivo 2]

## Pruebas
[Describir las pruebas realizadas]""",
            
            "note": """# Nota: [Título de la nota]

## Contenido
[Contenido principal de la nota]

## Fecha
[Fecha de la nota]

## Acciones Requeridas
[Si aplica, describir acciones necesarias]"""
        }
        
        return templates.get(entry_type, templates["note"])
