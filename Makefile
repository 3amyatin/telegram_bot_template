APP := app.py
VENV := .venv
ACTIVATE := source $(VENV)/bin/activate
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: help venv install clean run launch

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help        Show this help message"
	@echo "  venv        Create a virtual environment"
	@echo "  deps        Install dependencies"
	@echo "  clean       Clean up generated files"
	@echo "  run         Run the application"

venv: $(VENV)

$(VENV): 
	@echo Create a virtual environment
	python3 -m venv $(VENV)
	@echo "Virtual environment created."

deps: venv
	@echo Install dependencies
	$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

clean:
	@echo Clean up generated files	
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	@echo "Cleaned up."

run: deps
	@echo Run the application
	$(ACTIVATE) && $(PYTHON) $(APP)
	@echo "Application running."

launch: run