# Makefile for Odoo Development
# Make sure to activate your virtual environment before running these commands

# Variables
PYTHON = python
PIP = pip
ODOO_BIN = python odoo-bin
VENV_PATH = venv
CONFIG_FILE = .odoorc

# Colors for output (Windows PowerShell compatible)
GREEN = [32m
YELLOW = [33m
RED = [31m
BLUE = [34m
CYAN = [36m
NC = [0m

.PHONY: help install install-dev activate run run-dev run-update run-init run-shell test clean lint format requirements-update

# Default target
help:
	@powershell -Command "Write-Host 'Odoo Development Makefile' -ForegroundColor Green"
	@powershell -Command "Write-Host ''"
	@powershell -Command "Write-Host 'Available targets:' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  help             - Show this help message'"
	@powershell -Command "Write-Host '  install          - Install production requirements'"
	@powershell -Command "Write-Host '  install-dev      - Install development requirements (if available)'"
	@powershell -Command "Write-Host '  run              - Run Odoo server' -ForegroundColor Cyan"
	@powershell -Command "Write-Host '  run-dev          - Run Odoo server with --dev=all flag' -ForegroundColor Cyan"
	@powershell -Command "Write-Host '  run-update       - Run Odoo server with module update'"
	@powershell -Command "Write-Host '  run-init         - Run Odoo server with database initialization'"
	@powershell -Command "Write-Host '  run-shell        - Run Odoo shell'"
	@powershell -Command "Write-Host '  test             - Run Odoo tests'"
	@powershell -Command "Write-Host '  clean            - Clean Python cache files'"
	@powershell -Command "Write-Host '  lint             - Run linting (if flake8 is installed)'"
	@powershell -Command "Write-Host '  format           - Format code (if black is installed)'"
	@powershell -Command "Write-Host '  requirements-update - Update requirements.txt with current installed packages'"
	@powershell -Command "Write-Host ''"
	@powershell -Command "Write-Host 'Virtual Environment:' -ForegroundColor Yellow"
	@powershell -Command "Write-Host '  Make sure to activate your virtual environment first:'"
	@powershell -Command "Write-Host '  .\\venv\\Scripts\\Activate.ps1' -ForegroundColor Green"

# Install production requirements
install:
	@powershell -Command "Write-Host 'Installing production requirements...' -ForegroundColor Green"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@powershell -Command "Write-Host 'Installation complete!' -ForegroundColor Green"

# Install development requirements (if dev requirements file exists)
install-dev: install
	@powershell -Command "Write-Host 'Installing development requirements...' -ForegroundColor Green"
	@if exist requirements-dev.txt ($(PIP) install -r requirements-dev.txt) else (powershell -Command "Write-Host 'No requirements-dev.txt found, installing common dev tools...' -ForegroundColor Yellow" && $(PIP) install black flake8 pytest)
	@powershell -Command "Write-Host 'Development installation complete!' -ForegroundColor Green"

# Run Odoo server
run:
	@powershell -Command "Write-Host 'Starting Odoo server...' -ForegroundColor Cyan"
	$(ODOO_BIN) --config=$(CONFIG_FILE)

# Run Odoo server with development flags
run-dev:
	@powershell -Command "Write-Host 'Starting Odoo server in development mode...' -ForegroundColor Cyan"
	$(ODOO_BIN) --config=$(CONFIG_FILE) --dev=all

# Run Odoo server with module update
run-update:
	@powershell -Command "Write-Host 'Starting Odoo server with module update...' -ForegroundColor Yellow"
	$(ODOO_BIN) --config=$(CONFIG_FILE) --update=all --stop-after-init

# Run Odoo server with database initialization
run-init:
	@powershell -Command "Write-Host 'Initializing Odoo database...' -ForegroundColor Yellow"
	$(ODOO_BIN) --config=$(CONFIG_FILE) --init=base --stop-after-init

# Run Odoo shell
run-shell:
	@powershell -Command "Write-Host 'Starting Odoo shell...' -ForegroundColor Magenta"
	$(ODOO_BIN) shell --config=$(CONFIG_FILE)

# Run tests
test:
	@powershell -Command "Write-Host 'Running Odoo tests...' -ForegroundColor Blue"
	$(ODOO_BIN) --config=$(CONFIG_FILE) --test-enable --stop-after-init

# Clean Python cache files
clean:
	@powershell -Command "Write-Host 'Cleaning Python cache files...' -ForegroundColor Yellow"
	@if exist __pycache__ rmdir /s /q __pycache__
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@del /s /q *.pyc 2>nul || echo "No .pyc files to clean"
	@powershell -Command "Write-Host 'Clean complete!' -ForegroundColor Green"

# Run linting (if flake8 is available)
lint:
	@powershell -Command "Write-Host 'Running linting...' -ForegroundColor Blue"
	@flake8 --version >nul 2>&1 && flake8 . || powershell -Command "Write-Host 'flake8 not installed. Run make install-dev first.' -ForegroundColor Yellow"

# Format code (if black is available)
format:
	@powershell -Command "Write-Host 'Formatting code...' -ForegroundColor Blue"
	@black --version >nul 2>&1 && black . || powershell -Command "Write-Host 'black not installed. Run make install-dev first.' -ForegroundColor Yellow"

# Update requirements.txt with current installed packages
requirements-update:
	@powershell -Command "Write-Host 'Updating requirements.txt...' -ForegroundColor Cyan"
	$(PIP) freeze > requirements-current.txt
	@powershell -Command "Write-Host 'Current packages saved to requirements-current.txt' -ForegroundColor Yellow"
	@powershell -Command "Write-Host 'Compare with requirements.txt and update as needed' -ForegroundColor Yellow"

# Database management targets
db-create:
	@powershell -Command "Write-Host 'Creating database...' -ForegroundColor Green"
	$(ODOO_BIN) --config=$(CONFIG_FILE) -d odoo --stop-after-init

db-drop:
	@powershell -Command "Write-Host 'Dropping database...' -ForegroundColor Red"
	$(ODOO_BIN) --config=$(CONFIG_FILE) -d odoo --stop-after-init --dev=all

# Quick development server restart
restart: clean run-dev 