from setuptools import setup, find_packages
import os

# Leer README para la descripción larga
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="memoria-cursor",
    version="1.0.6",
    description="Sistema de memoria para agentes LLM - Herramienta para registrar información relevante del desarrollo de proyectos",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Juan Gabriel Juara",
    author_email="jgjuara@gmail.com",
    url="https://github.com/jgjuara/memoria-cursor",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",        # Para CLI
        "jsonschema>=3.0.0",   # Validación JSON
        "rich>=10.0.0",        # Output colorido y tablas
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
            "black>=21.0.0",
            "flake8>=3.8.0",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "memoria=memoria_cursor.cli:main",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Documentation",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Text Processing :: Markup",
    ],
    keywords="memory, llm, agents, development, documentation, git, project-management",
    project_urls={
        "Bug Reports": "https://github.com/jgjuara/memoria-cursor/issues",
        "Source": "https://github.com/jgjuara/memoria-cursor",
        "Documentation": "https://github.com/jgjuara/memoria-cursor#readme",
    },
)
