.PHONY: help install install-dev test lint format clean build publish

help: ## Mostrar esta ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias de producción
	pip install -e .

install-dev: ## Instalar dependencias de desarrollo
	pip install -e ".[dev]"

test: ## Ejecutar pruebas
	pytest tests/ -v --cov=memoria_cursor

lint: ## Ejecutar linter
	flake8 memoria_cursor/ tests/
	mypy memoria_cursor/

format: ## Formatear código
	black memoria_cursor/ tests/
	isort memoria_cursor/ tests/

clean: ## Limpiar archivos generados
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build: ## Construir paquete
	python -m build

publish: ## Publicar en PyPI (requiere configuración)
	python -m twine upload dist/*

check: ## Verificar paquete antes de publicar
	python -m twine check dist/*

docs: ## Generar documentación
	sphinx-build -b html docs/ docs/_build/html

dev-install: ## Instalar en modo desarrollo
	pip install -e ".[dev,docs]"

quick-test: ## Prueba rápida del CLI
	memoria --help
	memoria init --help
	memoria create --help
	memoria list --help
	memoria export --help
