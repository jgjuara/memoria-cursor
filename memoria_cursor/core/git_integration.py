"""
Integración automática con Git para capturar información del repositorio.
"""

import subprocess
from typing import Optional, Dict, Any
from pathlib import Path


class GitIntegration:
    """
    Clase para obtener información automática de Git del repositorio actual.
    
    Captura:
    - Commit actual y mensaje
    - Rama de trabajo
    - Estado del repositorio (limpio/sucio)
    """
    
    def __init__(self, project_root: str = "."):
        """
        Inicializar integración con Git.
        
        Args:
            project_root: Ruta raíz del proyecto
        """
        self.project_root = Path(project_root).resolve()
    
    def is_git_repository(self) -> bool:
        """Verificar si el directorio es un repositorio Git."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_git_info(self) -> Optional[Dict[str, Any]]:
        """
        Obtener información completa de Git.
        
        Returns:
            Diccionario con información de Git o None si no es repositorio
        """
        if not self.is_git_repository():
            return None
        
        try:
            git_info = {}
            
            # Commit actual
            commit_result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=5
            )
            if commit_result.returncode == 0:
                git_info['current_commit'] = commit_result.stdout.strip()[:7]
            
            # Mensaje del commit
            message_result = subprocess.run(
                ['git', 'log', '-1', '--pretty=format:%s'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=5
            )
            if message_result.returncode == 0:
                git_info['commit_message'] = message_result.stdout.strip()
            
            # Rama actual
            branch_result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=5
            )
            if branch_result.returncode == 0:
                git_info['branch'] = branch_result.stdout.strip()
            
            # Estado del repositorio
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=5
            )
            git_info['is_clean'] = status_result.returncode == 0 and not status_result.stdout.strip()
            
            # Información adicional del repositorio
            remote_result = subprocess.run(
                ['git', 'remote', 'get-url', 'origin'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=5
            )
            if remote_result.returncode == 0:
                git_info['remote_url'] = remote_result.stdout.strip()
            
            return git_info if git_info else None
            
        except subprocess.TimeoutExpired:
            return None
        except Exception:
            return None
    
    def get_current_commit(self) -> Optional[str]:
        """Obtener hash del commit actual."""
        git_info = self.get_git_info()
        return git_info.get('current_commit') if git_info else None
    
    def get_current_branch(self) -> Optional[str]:
        """Obtener rama actual."""
        git_info = self.get_git_info()
        return git_info.get('branch') if git_info else None
    
    def is_repository_clean(self) -> Optional[bool]:
        """Verificar si el repositorio está limpio."""
        git_info = self.get_git_info()
        return git_info.get('is_clean') if git_info else None
    
    def get_commit_message(self) -> Optional[str]:
        """Obtener mensaje del commit actual."""
        git_info = self.get_git_info()
        return git_info.get('commit_message') if git_info else None
    
    def get_remote_url(self) -> Optional[str]:
        """Obtener URL del repositorio remoto."""
        git_info = self.get_git_info()
        return git_info.get('remote_url') if git_info else None
    
    def get_file_status(self, file_path: str) -> Optional[str]:
        """
        Obtener estado de un archivo específico en Git.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Estado del archivo (M, A, D, R, C, U, etc.) o None
        """
        if not self.is_git_repository():
            return None
        
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain', '--', file_path],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=5
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # El primer carácter indica el estado del staging area
                # El segundo carácter indica el estado del working directory
                status = result.stdout.strip().split()[0]
                return status
            
            return None
            
        except (subprocess.TimeoutExpired, Exception):
            return None
    
    def get_recent_commits(self, limit: int = 5) -> Optional[list]:
        """
        Obtener commits recientes.
        
        Args:
            limit: Número máximo de commits a obtener
            
        Returns:
            Lista de commits recientes o None
        """
        if not self.is_git_repository():
            return None
        
        try:
            result = subprocess.run(
                ['git', 'log', f'-{limit}', '--pretty=format:%h|%s|%an|%ad', '--date=short'],
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=10
            )
            
            if result.returncode == 0:
                commits = []
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split('|')
                        if len(parts) >= 4:
                            commits.append({
                                'hash': parts[0],
                                'message': parts[1],
                                'author': parts[2],
                                'date': parts[3]
                            })
                return commits
            
            return None
            
        except (subprocess.TimeoutExpired, Exception):
            return None
