PYTHON := python3
POETRY := poetry

.PHONY: install install-dev run lint test type-check security-scan precommit hooks format check all

install:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e .

install-dev:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e .[dev]

run:
	uvicorn ssdlc_demo.main:app --host 0.0.0.0 --port 8000 --reload

format:
	black src tests
	isort src tests

lint:
	flake8 src tests

type-check:
	mypy src

test:
	pytest -q

security-scan:
	bandit -r src -q -lll
	pip-audit || true

precommit:
	pre-commit run --all-files

hooks:
	pre-commit install

check: format lint type-check test security-scan precommit

all: install-dev check 