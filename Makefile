# Makefile for Odoo Development
# Cross-platform compatible with Windows and Linux
# Make sure to activate your virtual environment before running these commands

# Variables
PYTHON = python
PIP = pip
ODOO_BIN = python odoo-bin
VENV_PATH = venv
CONFIG_FILE = .odoorc

# Detect operating system
UNAME_S := $(shell uname -s 2>/dev/null || echo "Windows")

# Colors for output (cross-platform)
ifeq ($(UNAME_S),Linux)
	GREEN = \033[32m
	YELLOW = \033[33m
	RED = \033[31m
	BLUE = \033[34m
	CYAN = \033[36m
	NC = \033[0m
	ECHO = printf
else ifeq ($(UNAME_S),Darwin)
	GREEN = \033[32m
	YELLOW = \033[33m
	RED = \033[31m
	BLUE = \033[34m
	CYAN = \033[36m
	NC = \033[0m
	ECHO = printf
else
	GREEN = [32m
	YELLOW = [33m
	RED = [31m
	BLUE = [34m
	CYAN = [36m
	NC = [0m
	ECHO = powershell -Command "Write-Host"
endif

.PHONY: help install install-dev activate run run-dev run-update run-init run-shell test clean lint format requirements-update

# Default target
help:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(GREEN)Odoo Development Makefile$(NC)\n"
	@$(ECHO) "\n"
	@$(ECHO) "$(YELLOW)Available targets:$(NC)\n"
	@$(ECHO) "  help             - Show this help message\n"
	@$(ECHO) "  install          - Install production requirements\n"
	@$(ECHO) "  install-dev      - Install development requirements (if available)\n"
	@$(ECHO) "  $(CYAN)run              - Run Odoo server$(NC)\n"
	@$(ECHO) "  $(CYAN)run-dev          - Run Odoo server with --dev=all flag$(NC)\n"
	@$(ECHO) "  run-update       - Run Odoo server with module update\n"
	@$(ECHO) "  run-init         - Run Odoo server with database initialization\n"
	@$(ECHO) "  run-shell        - Run Odoo shell\n"
	@$(ECHO) "  test             - Run Odoo tests\n"
	@$(ECHO) "  clean            - Clean Python cache files\n"
	@$(ECHO) "  lint             - Run linting (if flake8 is installed)\n"
	@$(ECHO) "  format           - Format code (if black is installed)\n"
	@$(ECHO) "  requirements-update - Update requirements.txt with current installed packages\n"
	@$(ECHO) "\n"
	@$(ECHO) "$(YELLOW)Virtual Environment:$(NC)\n"
	@$(ECHO) "  Make sure to activate your virtual environment first:\n"
	@$(ECHO) "  $(GREEN)source venv/bin/activate$(NC)\n"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(GREEN)Odoo Development Makefile$(NC)\n"
	@$(ECHO) "\n"
	@$(ECHO) "$(YELLOW)Available targets:$(NC)\n"
	@$(ECHO) "  help             - Show this help message\n"
	@$(ECHO) "  install          - Install production requirements\n"
	@$(ECHO) "  install-dev      - Install development requirements (if available)\n"
	@$(ECHO) "  $(CYAN)run              - Run Odoo server$(NC)\n"
	@$(ECHO) "  $(CYAN)run-dev          - Run Odoo server with --dev=all flag$(NC)\n"
	@$(ECHO) "  run-update       - Run Odoo server with module update\n"
	@$(ECHO) "  run-init         - Run Odoo server with database initialization\n"
	@$(ECHO) "  run-shell        - Run Odoo shell\n"
	@$(ECHO) "  test             - Run Odoo tests\n"
	@$(ECHO) "  clean            - Clean Python cache files\n"
	@$(ECHO) "  lint             - Run linting (if flake8 is installed)\n"
	@$(ECHO) "  format           - Format code (if black is installed)\n"
	@$(ECHO) "  requirements-update - Update requirements.txt with current installed packages\n"
	@$(ECHO) "\n"
	@$(ECHO) "$(YELLOW)Virtual Environment:$(NC)\n"
	@$(ECHO) "  Make sure to activate your virtual environment first:\n"
	@$(ECHO) "  $(GREEN)source venv/bin/activate$(NC)\n"
else
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
endif

# Install production requirements
install:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(GREEN)Installing production requirements...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@$(ECHO) "$(GREEN)Installation complete!$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(GREEN)Installing production requirements...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@$(ECHO) "$(GREEN)Installation complete!$(NC)"
else
	@powershell -Command "Write-Host 'Installing production requirements...' -ForegroundColor Green"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@powershell -Command "Write-Host 'Installation complete!' -ForegroundColor Green"
endif

# Install development requirements (if dev requirements file exists)
install-dev: install
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(GREEN)Installing development requirements...$(NC)"
	@if [ -f requirements-dev.txt ]; then $(PIP) install -r requirements-dev.txt; else echo "$(YELLOW)No requirements-dev.txt found, installing common dev tools...$(NC)" && $(PIP) install black flake8 pytest; fi
	@$(ECHO) "$(GREEN)Development installation complete!$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(GREEN)Installing development requirements...$(NC)"
	@if [ -f requirements-dev.txt ]; then $(PIP) install -r requirements-dev.txt; else echo "$(YELLOW)No requirements-dev.txt found, installing common dev tools...$(NC)" && $(PIP) install black flake8 pytest; fi
	@$(ECHO) "$(GREEN)Development installation complete!$(NC)"
else
	@powershell -Command "Write-Host 'Installing development requirements...' -ForegroundColor Green"
	@if exist requirements-dev.txt ($(PIP) install -r requirements-dev.txt) else (powershell -Command "Write-Host 'No requirements-dev.txt found, installing common dev tools...' -ForegroundColor Yellow" && $(PIP) install black flake8 pytest)
	@powershell -Command "Write-Host 'Development installation complete!' -ForegroundColor Green"
endif

# Run Odoo server
run:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(CYAN)Starting Odoo server...$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(CYAN)Starting Odoo server...$(NC)"
else
	@powershell -Command "Write-Host 'Starting Odoo server...' -ForegroundColor Cyan"
endif
	$(ODOO_BIN) --config=$(CONFIG_FILE)

# Run Odoo server with development flags
run-dev:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(CYAN)Starting Odoo server in development mode...$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(CYAN)Starting Odoo server in development mode...$(NC)"
else
	@powershell -Command "Write-Host 'Starting Odoo server in development mode...' -ForegroundColor Cyan"
endif
	$(ODOO_BIN) --config=$(CONFIG_FILE) --dev=all

# Run Odoo server with module update
run-update:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(YELLOW)Starting Odoo server with module update...$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(YELLOW)Starting Odoo server with module update...$(NC)"
else
	@powershell -Command "Write-Host 'Starting Odoo server with module update...' -ForegroundColor Yellow"
endif
	$(ODOO_BIN) --config=$(CONFIG_FILE) -d odoo --update=smart_engagement --stop-after-init

# Run Odoo server with database initialization
run-init:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(YELLOW)Initializing Odoo database...$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(YELLOW)Initializing Odoo database...$(NC)"
else
	@powershell -Command "Write-Host 'Initializing Odoo database...' -ForegroundColor Yellow"
endif
	$(ODOO_BIN) --config=$(CONFIG_FILE) -d odoo --init=smart_engagement --stop-after-init

# Run Odoo shell
run-shell:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(BLUE)Starting Odoo shell...$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(BLUE)Starting Odoo shell...$(NC)"
else
	@powershell -Command "Write-Host 'Starting Odoo shell...' -ForegroundColor Magenta"
endif
	$(ODOO_BIN) shell --config=$(CONFIG_FILE)

# Run tests
test:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(BLUE)Running Odoo tests...$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(BLUE)Running Odoo tests...$(NC)"
else
	@powershell -Command "Write-Host 'Running Odoo tests...' -ForegroundColor Blue"
endif
	$(ODOO_BIN) --config=$(CONFIG_FILE) --test-enable --stop-after-init

# Clean Python cache files
clean:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(YELLOW)Cleaning Python cache files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@$(ECHO) "$(GREEN)Clean complete!$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(YELLOW)Cleaning Python cache files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@$(ECHO) "$(GREEN)Clean complete!$(NC)"
else
	@powershell -Command "Write-Host 'Cleaning Python cache files...' -ForegroundColor Yellow"
	@if exist __pycache__ rmdir /s /q __pycache__
	@for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
	@del /s /q *.pyc 2>nul || echo "No .pyc files to clean"
	@powershell -Command "Write-Host 'Clean complete!' -ForegroundColor Green"
endif

# Run linting (if flake8 is available)
lint:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(BLUE)Running linting...$(NC)"
	@which flake8 >/dev/null 2>&1 && flake8 . || echo "$(YELLOW)flake8 not installed. Run make install-dev first.$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(BLUE)Running linting...$(NC)"
	@which flake8 >/dev/null 2>&1 && flake8 . || echo "$(YELLOW)flake8 not installed. Run make install-dev first.$(NC)"
else
	@powershell -Command "Write-Host 'Running linting...' -ForegroundColor Blue"
	@flake8 --version >nul 2>&1 && flake8 . || powershell -Command "Write-Host 'flake8 not installed. Run make install-dev first.' -ForegroundColor Yellow"
endif

# Format code (if black is available)
format:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(BLUE)Formatting code...$(NC)"
	@which black >/dev/null 2>&1 && black . || echo "$(YELLOW)black not installed. Run make install-dev first.$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(BLUE)Formatting code...$(NC)"
	@which black >/dev/null 2>&1 && black . || echo "$(YELLOW)black not installed. Run make install-dev first.$(NC)"
else
	@powershell -Command "Write-Host 'Formatting code...' -ForegroundColor Blue"
	@black --version >nul 2>&1 && black . || powershell -Command "Write-Host 'black not installed. Run make install-dev first.' -ForegroundColor Yellow"
endif

# Update requirements.txt with current installed packages
requirements-update:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(CYAN)Updating requirements.txt...$(NC)"
	$(PIP) freeze > requirements-current.txt
	@$(ECHO) "$(YELLOW)Current packages saved to requirements-current.txt$(NC)"
	@$(ECHO) "$(YELLOW)Compare with requirements.txt and update as needed$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(CYAN)Updating requirements.txt...$(NC)"
	$(PIP) freeze > requirements-current.txt
	@$(ECHO) "$(YELLOW)Current packages saved to requirements-current.txt$(NC)"
	@$(ECHO) "$(YELLOW)Compare with requirements.txt and update as needed$(NC)"
else
	@powershell -Command "Write-Host 'Updating requirements.txt...' -ForegroundColor Cyan"
	$(PIP) freeze > requirements-current.txt
	@powershell -Command "Write-Host 'Current packages saved to requirements-current.txt' -ForegroundColor Yellow"
	@powershell -Command "Write-Host 'Compare with requirements.txt and update as needed' -ForegroundColor Yellow"
endif

# Database management targets
db-create:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(GREEN)Creating database...$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(GREEN)Creating database...$(NC)"
else
	@powershell -Command "Write-Host 'Creating database...' -ForegroundColor Green"
endif
	$(ODOO_BIN) --config=$(CONFIG_FILE) -d odoo --stop-after-init

db-drop:
ifeq ($(UNAME_S),Linux)
	@$(ECHO) "$(RED)Dropping database...$(NC)"
else ifeq ($(UNAME_S),Darwin)
	@$(ECHO) "$(RED)Dropping database...$(NC)"
else
	@powershell -Command "Write-Host 'Dropping database...' -ForegroundColor Red"
endif
	$(ODOO_BIN) --config=$(CONFIG_FILE) -d odoo --stop-after-init --dev=all

# Quick development server restart
restart: clean run-dev 