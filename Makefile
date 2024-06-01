PYTHON = python
VENV_DIR = venv

install:
	$(PYTHON) -m pip install -r requirements.txt

venv:
	$(PYTHON) -m venv $(VENV_DIR)

.PHONY: lint_black
create_db:
	black --check .

.PHONY: lint_isort
create_db:
	isort . --check

.PHONY: lint_pylint
create_db:
	pylint .

.PHONY: tests
tests:
	$(PYTHON) -m pytest -s --cov-config=.coveragerc -p pytest_cov --cov=app --cov-append --cov-report=html test/


